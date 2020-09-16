""" GraphQL resolvers """

from typing import Any, Dict, List, Optional

from ariadne import (
    ObjectType,
    QueryType,
    MutationType,
    make_executable_schema,
    load_schema_from_path,
)
from pymongo import MongoClient

from ascmonitor.config import (
    mendeley_authinfo,
    mendeley_group_id,
    mongo_config,
    mongo_db,
    channel_auths,
)
from ascmonitor.publication_store import PublicationStore
from ascmonitor.event_store import EventStore
from ascmonitor.mendeleur import Mendeleur, MendeleyAuthInfo
from ascmonitor.poster import Poster
from ascmonitor.types import PublicationType, FilterList

mendeleur = Mendeleur(MendeleyAuthInfo(**mendeley_authinfo), mendeley_group_id)
mongo = MongoClient(**mongo_config)[mongo_db]
event_store = EventStore(mongo)
publication_store = PublicationStore(
    mendeleur=mendeleur, mongo=mongo, event_store=event_store
)
poster = Poster(
    mongo=mongo,
    event_store=event_store,
    publication_store=publication_store,
    auths=channel_auths,
)

# setup graphql
type_defs = load_schema_from_path("schema.graphql")

query = QueryType()

# pylint: disable=redefined-builtin,invalid-name
@query.field("publication")
def resolve_publication(*_, id: str) -> Optional[PublicationType]:
    """ Fetch publication by id """
    return publication_store.get_by_id(id)


@query.field("publicationBySlug")
def resolve_publication_by_slug(*_, slug: str) -> Optional[PublicationType]:
    """ Fetch publication by slug """
    return publication_store.get_by_slug(slug)


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

    # embed filterable fields
    for pub in pubs:
        for field in ["year", "journal", "disciplines", "keywords"]:
            pub[field] = {"value": pub[field]}

    # build edges
    edges = [{"cursor": pub["cursor"], "node": pub} for pub in pubs]

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
def resolve_publication_download_url(*_, id: str) -> Optional[str]:
    """ Resolves to download url or None on error """
    try:
        return publication_store.get_download_url(id)
    except:  # pylint: disable=bare-except
        return None


@query.field("authors")
def resolve_distinct_authors(*_) -> List[Dict[str, Any]]:
    """ Resolve distinct authors """
    authors = publication_store.get_distinct("authors")

    # unpack value
    for author in authors:
        for field in ["firstName", "lastName"]:
            if field in author["value"]:
                author[field] = author["value"][field]
        del author["value"]

    return authors


@query.field("years")
@query.field("journals")
@query.field("disciplines")
@query.field("keywords")
@query.field("queue")
def resolve_distinct_fields(_, info) -> List[Dict[str, Any]]:
    """ Resolve distinct values for a filterable field """
    field = {
        "[Year!]!": "year",
        "[Journal!]!": "journal",
        "[Discipline!]!": "disciplines",
        "[Keyword!]!": "keywords",
    }[str(info.return_type)]
    return publication_store.get_distinct(field)


def resolve_queue(*_, channel: str) -> Dict[str, Any]:
    """
    Show publications in queue for channel.
    Documents are ordered such that first is next doc to be posted.
    """
    raise NotImplementedError()


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
    docs = publication_store.get_publications(first=first)
    scores = [i / (len(docs) + 1) for i in range(1, len(docs) + 1)]
    recommendations = []
    for doc, score in zip(docs, scores[::-1]):
        recommendations.append({"score": score, "publication": doc})
    return recommendations


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
            author[field] = obj[field]

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
    try:
        publication_store.update()
    except Exception as exc:  # pylint: disable=broad-except
        return {"success": False, "message": repr(exc)}

    return {"success": True}


@mutation.field("appendToQueue")
def resolve_append_to_queue(*_, channel: str, publication: str):
    """ Append publication to queue for channel """
    raise NotImplementedError()


@mutation.field("moveUpInQueue")
def resolve_move_up_in_queue(*_, channel: str, publication: str):
    """ Move publication up in queue for channel """
    raise NotImplementedError()


@mutation.field("moveDownInQueue")
def resolve_move_down_in_queue(*_, channel: str, publication: str):
    """ Move publication down in queue for channel """
    raise NotImplementedError()


@mutation.field("removeFromQueue")
def resolve_remove_from_queue(*_, channel: str, publication: str):
    """ Remove publication from queue for channel """
    raise NotImplementedError()


@mutation.field("post")
def resolve_post(*_, channel: str, secret: str):
    """ Post next publication in queue for channel """
    # if post_secret_token:
    #     if secret != post_secret_token:
    #         abort(404)

    # try:
    #     response = poster.post(channel)
    # except KeyError:
    #     abort(404)

    # return jsonify(response)
    raise NotImplementedError()


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
)
