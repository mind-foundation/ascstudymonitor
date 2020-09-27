""" Starlette Web App """
from logging import getLogger
from textwrap import shorten

from ariadne.asgi import GraphQL
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from ascmonitor.config import development, sentry_dsn, client_dist_path
from ascmonitor.graphql import publication_store, schema

logger = getLogger(__name__)

if development:
    logger.info("Environment: development")
else:
    logger.info("Environment: production")

# initialize Sentry
if not development:
    sentry_sdk.init(dsn=sentry_dsn)

sitemap_folder = Jinja2Templates(directory="sitemap")
templates = Jinja2Templates(directory=client_dist_path)


def download_publication(request):
    """ Download a attached PDF publication """
    try:
        slug = request.path_params["slug"]
        download_url = publication_store.get_download_url(slug)
    except ValueError:
        return PlainTextResponse(
            "Could not find a download for this publication.", status_code=404
        )

    return RedirectResponse(url=download_url)


def single_publication(request):
    """
    Provides static link to publication.
    Includes meta tags.
    """
    slug = request.path_params["slug"]
    publication = publication_store.get_by_slug(slug)
    if publication is None:
        return PlainTextResponse("Could not find this publication", status_code=404)

    abstract = publication.abstract

    if not abstract:
        # placeholder abstract
        abstract = (
            "The ASC Study Monitor is a curated, freely accessible, "
            + "and regularly updated database of scholarly publications concerning "
            + "altered states of consciousness."
        )
    if len(abstract) > 240:
        # shorten abstract
        abstract = shorten(abstract, width=237, placeholder="...")

    # build url
    url = request.url_for("single_publication", slug=slug)

    # escape newlines in abstract
    abstract = abstract.replace("\n", "\\n").replace("\r", "\\r")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "abstract": abstract,
            "title": publication.title,
            "url": url,
            "initialPublication": publication.as_dict(),
        },
    )


def index(request):
    """ Serve the client with meta tags """
    return templates.TemplateResponse("index.html", {"request": request})


def sitemap(request):
    """ Build sitemap """
    urlset = [
        {"loc": request.url_for("single_publication", slug=pub.slug)}
        for pub in publication_store.get_publications()
    ]
    return sitemap_folder.TemplateResponse(
        "sitemap.xml", {"urlset": urlset, "request": request}
    )


graphql = GraphQL(schema, debug=development, context_value=lambda request: request)

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

routes = [
    Mount("/graphql", app=graphql),
    Route("/", endpoint=index),
    Route("/index.html", endpoint=index),
    Route(
        "/p/{slug}/download",
        endpoint=download_publication,
        name="download_publication",
    ),
    Route("/p/{slug}", endpoint=single_publication),
    Route("/sitemap.xml", endpoint=sitemap),
]

if development:
    routes.append(Mount("/", app=StaticFiles(directory=client_dist_path)))
else:
    # attach sentry
    middleware.append(Middleware(SentryAsgiMiddleware))

app = Starlette(debug=development, routes=routes, middleware=middleware)
