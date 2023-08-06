import os
import json


def credentials(url=None, token=None):
    """Get the credentials configuration from the
    `VOXJAR_APPLICATION_CREDENTIALS` environment variable.

    url can be overriden with the `VOXJAR_API_URL` environment variable.
    token can be overriden with the `VOXJAR_API_TOKEN` environment variable.

    Returns:
        dictionary: The contents of the :ref:`keyfile`.
    """
    if not url:
        url = os.getenv('VOXJAR_API_URL')

    if not token:
        token = os.getenv('VOXJAR_API_TOKEN')

    if not url or not token:
        creds = {}
        creds_file = os.getenv('VOXJAR_APPLICATION_CREDENTIALS')
        if creds_file:
            with open(creds_file, 'r') as f:
                creds = json.loads(f.read())

        if not url:
            url = creds.get('url', 'https://api.voxjar.com:9000')

        if not token:
            token = creds.get('token')

    return url, token
