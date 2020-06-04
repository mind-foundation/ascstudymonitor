""" Access the Mendeley Database """

from itertools import islice
import logging
import re
from typing import NamedTuple

from dateutil.parser import parse as parse_datetime
from mendeley import Mendeley
import requests
from slugify import slugify

from ascmonitor.config import required_fields, development

logger = logging.getLogger(__name__)


class MendeleyAuthInfo(NamedTuple):
    """ Authentication infos for Mendeley """

    client_id: str
    client_secret: str
    redirect_uri: str
    user: str
    password: str


class Mendeleur:
    """ Manages Mendeley session """

    def __init__(self, authinfo, group_id):
        """ Authenticate the Mendeley client """
        mendeley = Mendeley(
            client_id=authinfo.client_id,
            client_secret=authinfo.client_secret,
            redirect_uri=authinfo.redirect_uri,
        )

        auth = mendeley.start_authorization_code_flow()
        login_url = auth.get_login_url()

        response = requests.post(
            login_url,
            allow_redirects=False,
            data={"username": authinfo.user, "password": authinfo.password},
        )
        redirect_url = response.headers["Location"]
        redirect_url = redirect_url.replace("http://", "https://")

        self.session = auth.authenticate(redirect_url)
        self.group = self.session.groups.get(group_id)

    def all_documents(self):
        """
        Fetch the current library from mendeley.
        :returns: List of dicts with document bibliography
        """
        logger.info("Fetching fresh documents from mendeley")

        library = self.group.documents.iter(page_size=500, sort="created", order="desc", view="all")
        if development:
            library = islice(library, 0, 500)

        return list(self.transform_documents(doc for doc in library))

    def get_download_url(self, document_id):
        """ Return mendeley download url for a given document id """
        try:
            files = self.session.documents.get(document_id).files
            first_file = next(files.iter())
        except StopIteration:
            raise ValueError("Document has no file attached")
        return first_file.download_url

    def slugify(self, document):
        """ Put slug in document """
        first_id, *_ = document.json["id"].split("-")
        document.json["slug"] = (
            slugify(document.json["title"], max_length=60, word_boundary=True) + "-" + first_id
        )
        return document

    def extract_disciplines(self, document):
        """ Extract disciplines from document tags """
        disciplines = []
        if document.tags:
            for tag in document.tags:
                if tag.lower().startswith("disc:"):
                    disciplines.extend(tag[5:].split(":"))

            # strip bad characters
            disciplines = [re.sub(r"[^\w\s]", "", disc).strip() for disc in disciplines]

            document.json["disciplines"] = disciplines
        else:
            document.json["disciplines"] = []

        return document

    def ensure_authors(self, document):
        """ Ensure authors are present in document """
        if document.authors is None:
            document.json["authors"] = []
        return document

    def ensure_year(self, document):
        """ Ensure year is present or None """
        if document.year is None:
            document.json["year"] = None
        return document

    def cast_created(self, document):
        """ Cast created to datetime """
        created = document.json["created"].replace("Z", "")
        document.json["created"] = parse_datetime(created)

        return document

    def fix_file_attached(self, document):
        """ Test file_attached attribute """
        if document.file_attached:
            document.json["file_attached"] = bool(list(document.files.iter()))
        return document

    def filter_required_fields(self, document):
        """ Remove fields that are not required """
        document.json = {
            field: value for field, value in document.json.items() if field in required_fields
        }
        return document

    def transform_documents(self, documents):
        """ Generator that transforms mendeley documents """
        for document in documents:
            document = self.extract_disciplines(document)
            document = self.ensure_authors(document)
            document = self.ensure_year(document)
            document = self.fix_file_attached(document)
            document = self.slugify(document)
            document = self.cast_created(document)
            document = self.filter_required_fields(document)
            yield document.json
