""" Flask Web app """

from pymongo import MongoClient
from flask import (
    Flask,
    Response,
    abort,
    request,
    jsonify,
    redirect,
    render_template,
    send_from_directory,
)
from flask_cors import CORS

from ascmonitor.config import (
    mendeley_authinfo,
    mendeley_group_id,
    mongo_config,
    mongo_db,
    channel_auths,
    post_secret_token,
)
from ascmonitor.document_store import DocumentStore
from ascmonitor.event_store import EventStore
from ascmonitor.mendeleur import MendeleyAuthInfo
from ascmonitor.poster import Poster

app = Flask(__name__, static_folder="../static", template_folder="../templates")
CORS(app)

authinfo = MendeleyAuthInfo(**mendeley_authinfo)
mongo = MongoClient(**mongo_config)[mongo_db]
event_store = EventStore(mongo)
document_store = DocumentStore(
    authinfo=authinfo, group_id=mendeley_group_id, mongo=mongo, event_store=event_store
)
poster = Poster(event_store=event_store, auths=channel_auths)


@app.route("/documents.json")
def documents():
    """ Return documents as JSON """
    return jsonify(document_store.documents)


@app.route("/download/<doc_id>")
def download(doc_id):
    """ Download a attached PDF document """
    download_url = document_store.get_download_url(doc_id)
    return redirect(download_url, code=301)


@app.route("/update")
def update():
    """ Update bibliography """
    document_store.update()
    return Response("success", mimetype="text/plain")


@app.route("/queue")
def queue():
    """ Show current post queue """
    n_visible = 20
    docs = list(poster.queue)
    visible, hidden = docs[:n_visible], docs[n_visible:]
    entries = "\n".join(d["title"] for d in visible)
    rest = f"\n ... and {len(hidden)} more ..."
    return Response(entries + rest, mimetype="text/plain")


@app.route("/post/<channel>")
def post(channel):
    """
    Send out posts about new papers.
    Must be secure endpoint.
    """
    if post_secret_token:
        token = request.args.get("token")
        if token != post_secret_token:
            abort(404)

    poster.post(channel)


@app.route("/publication/<doc_slug>")
def publication(doc_slug):
    """
    Provides static link to document.
    Includes meta tags.
    """
    document = document_store.get_by_slug(doc_slug)
    if document is None:
        abort(404)
    return render_template("stub.html", document=document)


if app.env != "production":

    @app.route("/static/<path:path>")
    def send_js(path):
        """ Send static js in development """
        return send_from_directory("static", "path")

    @app.route("/")
    def browser():
        """ Show the table as HTML """
        return app.send_static_file("index.html")
