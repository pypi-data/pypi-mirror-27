import json

import requests

import opbeat_django.conf

BASE_URL = "https://intake.opbeat.com/api/v1"


class OpbeatAPI(object):
    """
    Simple Opbeat API wrapper.
    """
    def __init__(self, **kwargs):
        self.app_id = opbeat_django.conf.APP_ID
        self.org_id = opbeat_django.conf.ORGANIZATION_ID
        self.token = opbeat_django.conf.SECRET_TOKEN

        # kwargs can override settings
        self.base_url = kwargs.get("base_url", BASE_URL).rstrip('/')
        self.app_id = kwargs.get("app_id", self.app_id)
        self.org_id = kwargs.get("org_id", self.org_id)
        self.token = kwargs.get("token", self.token)

        if (
                self.app_id is None or
                self.org_id is None or
                self.token is None
        ):
            raise OBError("Opbeat settings are missing")

        self.app_url = self._app_url()

    def _app_url(self):
        return (
            "{api.base_url}/organizations/{api.org_id}/apps/{api.app_id}/"
        ).format(api=self)

    def _request(self, url, data):
        print(data)
        response = requests.post(
            url,
            data=json.dumps(data),
            headers={
                'Authorization': 'Bearer {api.token}'.format(api=self),
                'Content-Type': 'application/json',
            },
        )
        response.raise_for_status()
        return response

    def release(self, **kwargs):
        """
        Send a release notification.

        Required argument: rev, status
        Optional arguments: branch, machine
        """
        return self._request(
            self.app_url + 'releases/',
            data=kwargs,
        )

    def error(self, **kwargs):
        """
        Send an error notification.

        Required arguments: message
        Optional arguments: see api documentation
        """
        return self._request(
            self.app_url + 'errors/',
            data=kwargs,
        )


class OBError(Exception):
    """
    Base API error.
    """
    pass


class OBConfigError(OBError):
    """
    API client configuration error, like missing id or token.
    """
    pass
