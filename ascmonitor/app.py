""" Flask Web app """

from pymongo import MongoClient
from flask import Flask, Response, jsonify, redirect, send_from_directory
from flask_cors import CORS

from ascmonitor.config import mendeley_authinfo, mendeley_group_id, mongo_config, mongo_db
from ascmonitor.document_store import DocumentStore
from ascmonitor.event_store import EventStore
from ascmonitor.mendeleur import MendeleyAuthInfo
from ascmonitor.post_queue import PostQueue

app = Flask(__name__, static_folder="../static")
CORS(app)

authinfo = MendeleyAuthInfo(**mendeley_authinfo)
mongo = MongoClient(**mongo_config)[mongo_db]
event_store = EventStore(mongo)
document_store = DocumentStore(
    authinfo=authinfo, group_id=mendeley_group_id, mongo=mongo, event_store=event_store
)
post_queue = PostQueue(event_store=event_store)


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
    docs = list(post_queue)
    visible, hidden = docs[:n_visible], docs[n_visible:]
    entries = "\n".join(d["title"] for d in visible)
    rest = f"\n ... and {len(hidden)} more ..."
    return Response(entries + rest, mimetype="text/plain")


@app.route("/post")
def post():
    """
    Send out posts about new papers.
    Accepts channels as request parameter.
    Must be secure endpoint.
    """
    ...


@app.route("/publication/<doc_slug>")
def publication(doc_slug):
    """
    Provides static link to document.
    Includes meta tags.
    """
    ...


if app.env != "production":

    @app.route("/static/<path:path>")
    def send_js(path):
        """ Send static js in development """
        return send_from_directory("static", "path")

    @app.route("/")
    def browser():
        """ Show the table as HTML """
        return app.send_static_file("index.html")
