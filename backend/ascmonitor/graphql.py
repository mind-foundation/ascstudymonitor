""" GraphQL resolvers """

from typing import cast, Any, Dict, List, Optional

from ariadne import (
    ObjectType,
    QueryType,
    MutationType,
    UnionType,
    make_executable_schema,
    load_schema_from_path,
)
from pymongo import MongoClient
from humps import camelize, decamelize

from ascmonitor.channels import CHANNELS, PostSendException
from ascmonitor.config import (
    mendeley_authinfo,
    mendeley_group_id,
    mongo_config,
    mongo_db,
    channel_configs,
    post_secret_token,
)
from ascmonitor.publication_store import PublicationStore
from ascmonitor.publication import PublicationID
from ascmonitor.event_store import EventStore
from ascmonitor.events import EventKind, PostSuccessEvent
from ascmonitor.mendeleur import Mendeleur, MendeleyAuthInfo
from ascmonitor.ngram_store import NGramStore
from ascmonitor.post_queue import PostQueue, QueueEmptyException
from ascmonitor.poster import Poster
from ascmonitor.types import FilterList

mendeleur = Mendeleur(MendeleyAuthInfo(**mendeley_authinfo), mendeley_group_id)
mongo = MongoClient(**mongo_config)[mongo_db]
event_store = EventStore(mongo)
publication_store = PublicationStore(
    mendeleur=mendeleur, mongo=mongo, event_store=event_store
)
ngram_store = NGramStore(mongo=mongo)

# setup graphql
type_defs = load_schema_from_path("../schema.graphql")

query = QueryType()

# pylint: disable=redefined-builtin,invalid-name
@query.field("publication")
def resolve_publication(*_, id: PublicationID) -> Optional[Dict[str, Any]]:
    """ Fetch publication by id """
    pub = publication_store.get_by_id(id)
    if pub is None:
        return None
    return pub.as_gql_response()


@query.field("publicationBySlug")
def resolve_publication_by_slug(*_, slug: str) -> Optional[Dict[str, Any]]:
    """ Fetch publication by slug """
    pub = publication_store.get_by_slug(slug)
    if pub is None:
        return None
    return pub.as_gql_response()


@query.field("publications")
def resolve_publications(
    *_,
    search: Optional[str] = None,
    filters: Optional[FilterList] = None,
    first: Optional[int] = 25,
    after: Optional[str] = None,
) -> Dict[str, Any]:
    """ Query, filter and paginate publications """
    pubs = publication_store.get_publications(
        first=first, cursor=after, search=search, filters=filters
    )

    # build edges
    edges = [
        {
            "cursor": pub.encoded_cursor,
            "score": pub.score,
            "node": pub.as_gql_response(),
        }
        for pub in pubs
    ]

    # also return the query to make it available to child resolvers
    return {
        "search": search,
        "filters": filters,
        "edges": edges,
        "pageInfo": {
            "hasNextPage": first is not None and len(edges) >= first,
            "hasPreviousPage": False,
            "startCursor": after,
            "endCursor": edges[-1]["cursor"] if edges else None,
        },
    }


@query.field("publicationDownloadUrl")
def resolve_publication_download_url(*_, id: PublicationID) -> Optional[str]:
    """ Resolves to download url or None on error """
    try:
        return publication_store.get_download_url(id)
    except:  # pylint: disable=bare-except
        return None


@query.field("fieldSuggestions")
def resolve_field_suggestions(
    *_, search: str, first: int = 10, filters: Optional[FilterList] = None
) -> List[Dict[str, Any]]:
    """ Get suggestions for fields from the ngram store """
    # pylint: disable=unused-argument
    tokens = ngram_store.query(search, first)

    results = []
    for token in tokens:
        assert token.data is not None
        token.data["field"] = token.field  # for type resolver

        # unwind an author
        if token.field == "authors":
            author = token.data["value"]
            for field in ["first_name", "last_name"]:
                if field in author:
                    token.data[camelize(field)] = author[field]

        result = {
            "value": token.data,
            "field": token.field,
            "score": token.score,
        }
        results.append(result)

    return results


@query.field("authors")
def resolve_distinct_authors(*_) -> List[Dict[str, Any]]:
    """ Resolve distinct authors """
    authors = publication_store.get_distinct("authors")

    # unpack value
    for author in authors:
        for field in ["first_name", "last_name"]:
            if field in author["value"]:
                author[camelize(field)] = author["value"][field]

    return authors


@query.field("years")
@query.field("journals")
@query.field("disciplines")
@query.field("keywords")
def resolve_distinct_fields(_, info) -> List[Dict[str, Any]]:
    """ Resolve distinct values for a filterable field """
    field = {
        "[Year!]!": "year",
        "[Journal!]!": "journal",
        "[Discipline!]!": "disciplines",
        "[Keyword!]!": "keywords",
    }[str(info.return_type)]
    return publication_store.get_distinct(field)


@query.field("queue")
def resolve_queue(*_, channel: str) -> Optional[List[Dict[str, Any]]]:
    """
    Show publications in queue for channel.
    Documents are ordered such that first is next doc to be posted.
    """
    if channel not in channel_configs:
        return None

    queue = PostQueue(channel, mongo)

    ids = cast(List[PublicationID], queue.view())
    publications = publication_store.get_by_ids(ids)
    return [pub.as_gql_response() for pub in publications]


publications_connection = ObjectType("PublicationsConnection")


@publications_connection.field("totalCount")
def publications_total_count(obj, _info) -> int:
    """ Return the total count of a publications connection """
    search = obj["search"]
    filters = obj["filters"]
    return publication_store.get_publications_count(search, filters)


publication_type = ObjectType("Publication")


@publication_type.field("recommendations")
def resolve_recommendations(_source, _info, first: int) -> List[Dict[str, Any]]:
    """ Resolve recommended publications for source publication """
    pubs = publication_store.get_publications(first=first)
    scores = [i / (len(pubs) + 1) for i in range(1, len(pubs) + 1)]
    recommendations = []
    for pub, score in zip(pubs, scores[::-1]):
        recommendations.append({"score": score, "publication": pub.as_gql_response()})
    return recommendations


@publication_type.field("hasBeenPosted")
def resolve_has_been_posted(obj, _info, channel: str) -> bool:
    """ Resolve if publication has been posted before """
    id_ = obj["id"]
    events = event_store.query(id_, kinds=[EventKind.post_success])
    return any(cast(PostSuccessEvent, event).channel == channel for event in events)


author_type = ObjectType("Author")
year_type = ObjectType("Year")
journal_type = ObjectType("Journal")
discipline_type = ObjectType("Discipline")
keyword_type = ObjectType("Keyword")


@author_type.field("publicationCount")
def resolve_author_publication_count(obj, _info) -> int:
    """ Count the publications for an author """
    if "publicationCount" in obj:
        return obj["publicationCount"]

    author = {}
    for field in ["firstName", "lastName"]:
        if field in obj:
            author[decamelize(field)] = obj[field]

    return publication_store.count_publications("authors", author)


@year_type.field("publicationCount")
@journal_type.field("publicationCount")
@discipline_type.field("publicationCount")
@keyword_type.field("publicationCount")
def resolve_publication_count(obj, info) -> int:
    """ Count the publications for a filterable field """
    if "publicationCount" in obj:
        return obj["publicationCount"]

    value = obj["value"]
    field = {
        "Year": "year",
        "Journal": "journal",
        "Discipline": "disciplines",
        "Keyword": "keywords",
    }[info.parent_type.name]
    return publication_store.count_publications(field, value)


mutation = MutationType()


@mutation.field("updatePublications")
def resolve_update_publications(*_) -> Dict[str, Any]:
    """ Update the publications in the document store """
    publication_store.update()
    ngram_store.update(publication_store.get_tokens())
    return {"success": True}


@mutation.field("appendToQueue")
def resolve_append_to_queue(*_, channel: str, publication: str) -> Dict[str, Any]:
    """ Append publication to queue for channel """
    if channel not in CHANNELS:
        return {"success": False, "message": "Unsupported channel"}

    queue = PostQueue(channel, mongo)

    try:
        queue.append(publication)
    except (ValueError, RuntimeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True}


@mutation.field("moveUpInQueue")
def resolve_move_up_in_queue(*_, channel: str, publication: str) -> Dict[str, Any]:
    """ Move publication up in queue for channel """
    if channel not in channel_configs:
        return {"success": False, "message": "Unsupported channel"}

    queue = PostQueue(channel, mongo)

    try:
        queue.move_up(publication)
    except (ValueError, RuntimeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True}


@mutation.field("moveDownInQueue")
def resolve_move_down_in_queue(*_, channel: str, publication: str) -> Dict[str, Any]:
    """ Move publication down in queue for channel """
    if channel not in channel_configs:
        return {"success": False, "message": "Unsupported channel"}

    queue = PostQueue(channel, mongo)

    try:
        queue.move_down(publication)
    except (ValueError, RuntimeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True}


@mutation.field("removeFromQueue")
def resolve_remove_from_queue(*_, channel: str, publication: str) -> Dict[str, Any]:
    """ Remove publication from queue for channel """
    if channel not in channel_configs:
        return {"success": False, "message": "Unsupported channel"}

    queue = PostQueue(channel, mongo)

    try:
        queue.remove(publication)
    except (ValueError, RuntimeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True}


@mutation.field("post")
def resolve_post(_, info, channel: str, secret: str):
    """ Post next publication in queue for channel """
    if post_secret_token:
        if secret != post_secret_token:
            return {"success": False, "message": "Bad secret"}

    if channel not in CHANNELS:
        return {"success": False, "message": "Unsupported channel"}

    try:
        queue = PostQueue(channel, mongo)
        publication_id = cast(PublicationID, queue.pop())
        publication = publication_store.get_by_id(publication_id)

        if publication is None:
            return {"success": False, "message": "Queued publication is not in store"}

        url = info.context.url_for("single_publication", slug=publication.slug)
    except QueueEmptyException:
        return {
            "success": False,
            "message": f"Post queue is empty for channel {channel}",
        }

    try:
        poster = Poster(
            channel=CHANNELS[channel](**channel_configs.get(channel, {})),
            mongo=mongo,
            event_store=event_store,
            publication_store=publication_store,
        )
        sent_post = poster.post(publication, url)
    except PostSendException as error:
        return {"success": False, "message": error.message}

    return {
        "success": True,
        "publication": publication.id_,
        "created": sent_post.created,
        "postPayload": sent_post.payload,
        "postID": sent_post.id_,
        "response": sent_post.response,
    }


filterable_field = UnionType("FilterableField")


@filterable_field.type_resolver
def resolve_filterable_field_type(obj, *_):
    """ Type resolver a filterable field """
    return {
        "year": "Year",
        "journal": "Journal",
        "authors": "Author",
        "disciplines": "Discipline",
        "keywords": "Keyword",
    }[obj["field"]]


schema = make_executable_schema(
    type_defs,
    query,
    publication_type,
    publications_connection,
    author_type,
    year_type,
    journal_type,
    discipline_type,
    keyword_type,
    mutation,
    filterable_field,
)
