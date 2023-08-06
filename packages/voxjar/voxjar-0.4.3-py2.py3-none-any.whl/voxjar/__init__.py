import os
import json
from voxjar.push_request import PushRequest
import gql
from voxjar.transport import HttpTransport
import voxjar.auth


class Client(object):
    """Voxjar API client.

    Args:
        url (str, optional): The URL for the API.
        token (str, optional): The JWT authenticating this Client to the API.
        timeout (int, optional): The timeout for API calls.
    """

    def __init__(self, url=None, token=None, timeout=None):
        self.url, self.token = voxjar.auth.credentials(url=url, token=token)

        graphql_url = '{}/graphql'.format(self.url)
        self._client = gql.Client(
            transport=HttpTransport(graphql_url, token, timeout),
            fetch_schema_from_transport=True)

    def push_request(self, metadata, audio=None):
        """A file-like object used to enqueue a call audio file to be processed
        by Voxjar.

        Args:
            metadata (dict): The metadata for the call.
            audio (file): The raw audio bytes of the call.
        Returns:
            metadata (dict): The metadata for the uploaded call.
        Example:
            .. code:: python

                import datetime
                import requests
                import voxjar

                metadata = {
                    'identifier': 'callIdentifier',
                    'type': {
                        'identifier': 'typeIdentifier',
                        'name': 'typeName',
                    },
                    'timestamp': datetime.datetime.now(),
                    'direction': 'OUTGOING',  # or INCOMING
                    'agents': [{
                        'identifier': 'agentIdentifier',
                        'name': 'Agent Name',
                        'phoneNumber': 1234567890  # optional
                    }],
                    # optional
                    'customers': [{
                        'identifier': 'customerIdentifier',
                        'name': 'Customer Name',
                        'phoneNumber': 9876543210  # optional
                    }],
                    'disposition': {
                        'identifier': 'dispositionIdentifier',
                        'name': 'dispositionName',
                    },
                    'tags': ['tag1', 'tag2'],
                }

                client = voxjar.Client()

                r = requests.get('https://somesource.com', stream=True)
                with client.push_request(metadata) as push_request:
                    for chunk in r.iter_content(chunk_size=1024):
                        push_request.write(chunk)
                    push_request.push()

        """
        return PushRequest(self.token, metadata, audio=audio, url=self.url)

    def push(self, metadata, audio):
        """Enqueue a call to be processed by Voxjar.

        Args:
            metadata (dict): The metadata for the call.
            audio (file): The raw audio bytes of the call.
        Returns:
            metadata (dict): The metadata for the uploaded call.
        Example:
            .. code:: python

                import datetime
                import voxjar

                metadata = {
                    'identifier': 'callIdentifier',
                    'type': {
                        'identifier': 'typeIdentifier',
                        'name': 'typeName',
                    },
                    'timestamp': datetime.datetime.now(),
                    'direction': 'OUTGOING',  # or INCOMING
                    'agents': [{
                        'identifier': 'agentIdentifier',
                        'name': 'Agent Name',
                        'phoneNumber': 1234567890  # optional
                    }],
                    # optional
                    'customers': [{
                        'identifier': 'customerIdentifier',
                        'name': 'Customer Name',
                        'phoneNumber': 9876543210  # optional
                    }],
                    'disposition': {
                        'identifier': 'dispositionIdentifier',
                        'name': 'dispositionName',
                    },
                    'tags': ['tag1', 'tag2'],
                }

                client = voxjar.Client()

                with open('test.wav', 'rb') as f:
                    client.push(metadata, f)
        """
        with PushRequest(self.token, metadata, audio, self.url) as push_request:
            return push_request.push()

    def execute(self, document, *args, **kwargs):
        doc = gql.gql(document) if isinstance(document, str) else document
        return self._client.execute(doc, *args, **kwargs)
