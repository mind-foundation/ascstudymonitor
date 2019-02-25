""" Provides a Mendeley session """

import requests
from mendeley import Mendeley

import ascmonitor.bib_cache as cache


class Mendeleur:
    """ Access documents on mendeley """

    def __init__(self, client_id, client_secret, redirect_uri, user, password):
        self._authenticate(client_id, client_secret, redirect_uri, user, password)

    def _authenticate(self, client_id, client_secret, redirect_uri, user, password):
        mendeley = Mendeley(
            client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri
        )
        auth = mendeley.start_authorization_code_flow()
        login_url = auth.get_login_url()

        response = requests.post(
            login_url, allow_redirects=False, data={'username': user, 'password': password}
        )
        redirect_url = response.headers['Location']
        redirect_url = redirect_url.replace('http://', 'https://')

        self.session = auth.authenticate(redirect_url)

    @property
    def documents(self):
        """ Return documents as list """
        if cache.needs_update():
            documents = self._fetch_documents_from_mendeley()
            cache.update_documents(documents)
        else:
            documents = cache.get_documents()
        return documents

    def get_download_url(self, document_id):
        """ Return mendeley download url for a given document id """
        try:
            files = self.session.document_files(document_id).iter()
            first_file = next(files)
        except StopIteration:
            raise ValueError('Document has no file attached')
        return first_file.download_url

    def _fetch_documents_from_mendeley(self):
        """
        Fetch the current library from mendeley.
        :returns: List of dicts with document bibliography
        """
        library = self.session.documents.iter(sort='created', order='desc', view='all')
        return self._transform_documents(doc.json for doc in library)

    @staticmethod
    def _extract_disciplin(document):
        """ Extract disciplines from document tags """
        disciplines = []
        if 'tags' in document:
            tags = document['tags']
            for tag in tags:
                if tag.lower().startswith('disc:'):
                    disciplines.extend(tag[5:].split(''))
        return {**document, 'disciplines': disciplines}

    def _transform_documents(self, documents):
        """
        Apply various filters and transformations to the documents returned by mendeley
        """
        transformed = []
        for document in documents:
            document = self._extract_disciplin(document)
            transformed.append(document)
        return transformed
