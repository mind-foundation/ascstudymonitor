""" ASC Study Monitor Infrastructure """
__version__ = '0.1.0'

from flask import Flask, jsonify, redirect, abort

app = Flask(__name__, static_folder='../static')

from ascmonitor.config import mendeley
from ascmonitor.mendeleur import Mendeleur

mendeleur = Mendeleur(**mendeley)


@app.route('/documents.json')
def documents():
    """ Return documents as JSON """
    return jsonify(mendeleur.documents)


@app.route('/download/<doc_id>')
def download(doc_id):
    download_url = mendeleur.get_download_url(doc_id)
    return redirect(download_url, code=301)


@app.route('/download_backroom/<doc_id>')
def download_backroom(doc_id):
    return abort(404)


@app.route('/search_fulltext/<query>')
def search_fulltext(query):
    return abort(404)


@app.route('/')
def browser():
    """ Show the table as HTML """
    return app.send_static_file('index.html')


@app.route('/backroom')
def backroom():
    """ Show the table as HTML and give access to backroom downloads """
    return app.send_static_file('index.html')
