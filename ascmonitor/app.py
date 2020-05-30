""" Flask Web app """

from pymongo import MongoClient
from flask import Flask, Response, jsonify, redirect, send_from_directory
from flask_cors import CORS

from ascmonitor.config import mendeley_authinfo, mendeley_group_id, mongo_config, mongo_db
from ascmonitor.document_store import DocumentStore
from ascmonitor.mendeleur import MendeleyAuthInfo

app = Flask(__name__, static_folder="../static")
CORS(app)

authinfo = MendeleyAuthInfo(**mendeley_authinfo)
mongo = MongoClient(**mongo_config)[mongo_db]
document_store = DocumentStore(authinfo=authinfo, group_id=mendeley_group_id, mongo=mongo)


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
    ...


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
