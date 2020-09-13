""" Flask Web app """
from typing import Any, Dict, Optional

from ariadne import (
    ObjectType,
    QueryType,
    MutationType,
    graphql_sync,
    make_executable_schema,
    load_schema_from_path,
)
from ariadne.constants import PLAYGROUND_HTML
from pymongo import MongoClient
from flask import (
    Flask,
    abort,
    request,
    jsonify,
    redirect,
    render_template,
    render_template_string,
    send_from_directory,
    url_for,
)
from flask_cors import CORS

from ascmonitor.config import (
    mendeley_authinfo,
    mendeley_group_id,
    mongo_config,
    mongo_db,
    channel_auths,
    post_secret_token,
    development,
)
from ascmonitor.document_store import DocumentStore
from ascmonitor.event_store import EventStore
from ascmonitor.mendeleur import Mendeleur, MendeleyAuthInfo
from ascmonitor.poster import Poster
from ascmonitor.sitemap import sitemap_template
from ascmonitor.types import DocumentType, FilterList

static_folder = "../../client/dist/"
template_folder = static_folder
app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
CORS(app)

if development:
    app.logger.info("Environment: development")  # pylint: disable=no-member
else:
    app.logger.info("Environment: production")  # pylint: disable=no-member


mendeleur = Mendeleur(MendeleyAuthInfo(**mendeley_authinfo), mendeley_group_id)
mongo = MongoClient(**mongo_config)[mongo_db]
event_store = EventStore(mongo)
document_store = DocumentStore(
    mendeleur=mendeleur, mongo=mongo, event_store=event_store
)
poster = Poster(
    mongo=mongo,
    event_store=event_store,
    document_store=document_store,
    auths=channel_auths,
)


# setup graphql
type_defs = load_schema_from_path("schema.graphql")

query = QueryType()

# pylint: disable=redefined-builtin,invalid-name
@query.field("document")
def resolve_document(*_, id: str) -> Optional[DocumentType]:
    """ Fetch document by id """
    return document_store.get_by_id(id)


@query.field("documentBySlug")
def resolve_document_by_slug(*_, slug: str) -> Optional[DocumentType]:
    """ Fetch document by slug """
    return document_store.get_by_slug(slug)


@query.field("documents")
def resolve_documents(
    *_,
    query: Optional[str] = None,
    filters: Optional[FilterList] = None,
    first: Optional[int] = None,
    after: Optional[str] = None,
) -> Dict[str, Any]:
    """ Query, filter and paginate documents """
    docs = document_store.get_documents(first=first, cursor=after, filters=filters)
    edges = [{"cursor": doc["cursor"], "node": doc} for doc in docs]

    return {
        "edges": edges,
        "pageInfo": {
            "hasNextPage": first is not None and len(edges) >= first,
            "hasPreviousPage": False,
            "startCursor": after,
            "endCursor": edges[-1]["cursor"] if edges else None,
        },
    }


@query.field("documentDownloadUrl")
def resolve_document_download_url(*_, id: str) -> Optional[str]:
    """ Resolves to download url or None on error """
    try:
        return document_store.get_download_url(id)
    except:  # pylint: disable=bare-except
        return None


@query.field("queue")
def resolve_queue(*_, channel: str) -> Dict[str, Any]:
    """
    Show documents in queue for channel.
    Documents are ordered such that first is next doc to be posted.
    """
    raise NotImplementedError()


document = ObjectType("Document")


@document.field("recommendations")
def resolve_recommendations(obj, info_, first: int) -> Dict[str, Any]:
    """ Resolve recommendations for document """
    docs = document_store.get_documents(first=first)
    scores = [i / (len(docs) + 1) for i in range(1, len(docs) + 1)]
    recommendations = []
    for doc, score in zip(docs, scores[::-1]):
        recommendations.append({"score": score, "document": doc})
    return recommendations


mutation = MutationType()


@mutation.field("updateDocuments")
def resolve_update_documents(*_) -> Dict[str, Any]:
    """ Update the documents in the document store """
    try:
        document_store.update()
    except Exception as exc:  # pylint: disable=broad-except
        return {"success": False, "message": repr(exc)}

    return {"success": True}


@mutation.field("appendToQueue")
def resolve_append_to_queue(*_, channel: str, document: str):
    """ Append document to queue for channel """
    raise NotImplementedError()


@mutation.field("moveUpInQueue")
def resolve_move_up_in_queue(*_, channel: str, document: str):
    """ Move document up in queue for channel """
    raise NotImplementedError()


@mutation.field("moveDownInQueue")
def resolve_move_down_in_queue(*_, channel: str, document: str):
    """ Move document down in queue for channel """
    raise NotImplementedError()


@mutation.field("removeFromQueue")
def resolve_remove_from_queue(*_, channel: str, document: str):
    """ Remove document from queue for channel """
    raise NotImplementedError()


@mutation.field("post")
def resolve_post(*_, channel: str, secret: str):
    """ Post next document in queue for channel """
    # if post_secret_token:
    #     if secret != post_secret_token:
    #         abort(404)

    # try:
    #     response = poster.post(channel)
    # except KeyError:
    #     abort(404)

    # return jsonify(response)
    raise NotImplementedError()


schema = make_executable_schema(type_defs, query, document, mutation)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    """ GraphQL playground provided by ariadne """
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    """ Endpoint for GraphQL API """
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)

    status_code = 200 if success else 400
    return jsonify(result), status_code


@app.route("/documents/<id_>/download")
def download(id_):
    """ Download a attached PDF document """
    # TODO: error handling
    download_url = document_store.get_download_url(id_)
    return redirect(download_url, code=301)


@app.route("/p/<slug>")
def publication(slug):
    """
    Provides static link to document.
    Includes meta tags.
    """
    document = document_store.get_by_slug(slug)
    if document is None:
        abort(404)

    # shorten abstract
    try:
        abstract = document["abstract"]
        if len(abstract) > 240:
            paragraphs = abstract.split("\n")
            abstract = ""
            for par in paragraphs:
                abstract += "\n" + par
                if len(abstract) > 240:
                    break
    except KeyError:
        abstract = (
            "The ASC Study Monitor is a curated, freely accessible, "
            + "and regularly updated database of scholarly publications concerning "
            + "altered states of consciousness."
        )

    # build url
    url = url_for("publication", slug=slug, _external=True)

    # escape newlines in abstract
    abstract = abstract.replace("\n", "\\n").replace("\r", "\\r")

    return render_template(
        "index.html",
        abstract=abstract,
        title=document["title"],
        url=url,
        initial_publication=document,
    )


@app.route("/")
@app.route("/index.html")
def index():
    """ Show the table as HTML """
    return render_template("index.html")


@app.route("/sitemap.xml")
def sitemap():
    """ Build sitemap """
    urlset = [
        {"loc": url_for("publication", slug=d["slug"], _external=True)}
        for d in document_store.get_documents()
    ]
    return render_template_string(sitemap_template, urlset=urlset)


@app.route("/<path:path>")
def send_asset(path):
    """ Send static js in development """
    if not app.debug:
        # pylint: disable=no-member
        app.logger.warning("Sending static assed through flask while not in debug mode")
    return send_from_directory(static_folder, path)
