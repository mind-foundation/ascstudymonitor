""" Flask Web app """

from redis import Redis
from flask import Flask, Response, jsonify, redirect, abort, send_from_directory

from ascmonitor.config import mendeley_authinfo, mendeley_group_id, redis_config
from ascmonitor.document_store import DocumentStore
from ascmonitor.mendeleur import MendeleyAuthInfo

app = Flask(__name__, static_folder='../static')

authinfo = MendeleyAuthInfo(**mendeley_authinfo)
redis = Redis(**redis_config)
document_store = DocumentStore(authinfo=authinfo, group_id=mendeley_group_id, redis=redis)


@app.route('/documents.json')
def documents():
    """ Return documents as JSON """
    return jsonify(document_store.documents)


@app.route('/download/<doc_id>')
def download(doc_id):
    """ Download a attached PDF document """
    download_url = document_store.get_download_url(doc_id)
    return redirect(download_url, code=301)


@app.route('/download_backroom/<doc_id>')
def download_backroom(doc_id):
    """ TODO: download page with sci-hub links """
    return abort(404)


@app.route('/search_fulltext/<query>')
def search_fulltext(query):
    """ TODO: fulltext search in file archive """
    return abort(404)


@app.route('/update')
def update():
    """ Update bibliography """
    document_store.update()
    return Response('success', mimetype='text/plain')


@app.route('/static/<path:path>')
def send_js(path):
    print('match')
    return send_from_directory('static', 'path')


@app.route("/")
def browser():
    """ Show the table as HTML """
    return app.send_static_file('index.html')


@app.route('/backroom')
def backroom():
    """ Show the table as HTML and give access to backroom downloads """
    return app.send_static_file('index.html')


# alias for AWS
application = app

if __name__ == '__main__':
    application.run()
