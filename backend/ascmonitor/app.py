""" Flask Web app """
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
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

from ascmonitor.config import development
from ascmonitor.graphql import document_store, schema
from ascmonitor.sitemap import sitemap_template

static_folder = "../../client/dist/"
template_folder = static_folder
app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
CORS(app)

if development:
    app.logger.info("Environment: development")  # pylint: disable=no-member
else:
    app.logger.info("Environment: production")  # pylint: disable=no-member


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


@app.route("/publications/<id_>/download")
def download(id_):
    """ Download a attached PDF document """
    # TODO: error handling
    download_url = document_store.get_download_url(id_)
    return redirect(download_url, code=301)


@app.route("/p/<slug>")
def single_publication(slug):
    """
    Provides static link to document.
    Includes meta tags.
    """
    publication = document_store.get_by_slug(slug)
    if publication is None:
        abort(404)

    # shorten abstract
    try:
        abstract = publication["abstract"]
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
        title=publication["title"],
        url=url,
        initial_publication=publication,
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
        {"loc": url_for("single_publication", slug=d["slug"], _external=True)}
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
