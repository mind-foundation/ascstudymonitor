""" Store documents in Mendeley """

from typing import NamedTuple
import requests
from mendeley import Mendeley

from ascmonitor.config import cache_expires
from ascmonitor.document_cache import DocumentCache


class MendeleyAuthInfo(NamedTuple):
    """ Authentication infos for Mendeley """

    client_id: str
    client_secret: str
    redirect_uri: str
    user: str
    password: str


def extract_disciplin(document):
    """ Extract disciplines from document tags """
    disciplines = []
    if 'tags' in document:
        tags = document['tags']
        for tag in tags:
            if tag.lower().startswith('disc:'):
                disciplines.extend(tag[5:].split(''))
    return {**document, 'disciplines': disciplines}


def transform_documents(documents):
    """ Streaming generator that transforms mendeley documents """
    for document in documents:
        document = extract_disciplin(document)
        yield document


class Mendeleur:
    """ Manages Mendeley session """

    def __init__(self, authinfo):
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
            data={'username': authinfo.user, 'password': authinfo.password},
        )
        redirect_url = response.headers['Location']
        redirect_url = redirect_url.replace('http://', 'https://')

        self.session = auth.authenticate(redirect_url)

    def all_documents(self):
        """
        Fetch the current library from mendeley.
        :returns: List of dicts with document bibliography
        """
        library = self.session.documents.iter(sort='created', order='desc', view='all')
        return list(transform_documents(doc.json for doc in library))

    def get_download_url(self, document_id):
        """ Return mendeley download url for a given document id """
        try:
            files = self.session.document_files(document_id).iter()
            first_file = next(files)
        except StopIteration:
            raise ValueError('Document has no file attached')
        return first_file.download_url


class DocumentStore:
    """ Access to documents """

    def __init__(self, authinfo, redis):
        self._mendeley = Mendeleur(authinfo)
        self._cache = DocumentCache(redis, self._mendeley.all_documents, cache_expires)

    @property
    def documents(self):
        """ Return documents """
        return self._cache.get()

    def update(self):
        """ Force update """
        self._cache.expire()
        self._cache.get()

    def get_download_url(self, document_id):
        """ Get download link for specified document """
        return self._mendeley.get_download_url(document_id)
