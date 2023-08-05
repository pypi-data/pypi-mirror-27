"""Client library for Direqt Ads API."""
import json
import logging
import os
import uuid

import requests

import rbm

logger = logging.getLogger(__name__)

_DEFAULT_ENDPOINT = 'https://ads.direqt.io'
_DEFAULT_USER_AGENT = 'unknown'

_AD_FORMAT_RBM10 = 'RBMV1.0'
_DEFAULT_AD_FORMAT = _AD_FORMAT_RBM10
_VALID_AD_FORMATS = [_AD_FORMAT_RBM10]

_DEFAULT_RBM_ENDPOINT = 'https://rcsbusinessmessaging.googleapis.com'


class DireqtClient(object):
    """Client for the Direqt ad server."""

    def __init__(self, api_key, ad_format=_DEFAULT_AD_FORMAT, user_agent=_DEFAULT_USER_AGENT, **kwargs):
        """Initializes a DireqtClient.

        Args:
            api_key: A string containing your Direqt API key.
            format: Must be 'RBMv1.0'
            user_agent: An arbitrary string containing only ASCII characters
                that will be used to identify your application. If not set,
                defaults to "unknown".
            **kwargs: Optional keyword arguments.

        Keyword Arguments:
            None defined.
        """
        super(DireqtClient, self).__init__()

        if ad_format not in _VALID_AD_FORMATS:
            raise NotImplementedError(
                'The provided ad format "%s" is invalid. Accepted formats are: %s'
                % (format, _VALID_AD_FORMATS))

        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            import requests_toolbelt.adapters.appengine
            requests_toolbelt.adapters.appengine.monkeypatch()

        self.api_key = api_key
        self.fmt = ad_format
        self.user_agent = user_agent
        self.endpoint = kwargs.get('endpoint', _DEFAULT_ENDPOINT)               # private
        self.http = kwargs.get('http', requests)                                # private
        self.rbm_endpoint = kwargs.get('rbm_endpoint', _DEFAULT_RBM_ENDPOINT)   # private
        self.rbm_http = kwargs.get('rbm_http', rbm.http)

    def fetch(self, ad_unit, msisdn, targeting=None):
        """Fetch an ad from the Direqt Ads API.

        Args:
            ad_unit: An ad unit code configured in your project.
            session: A string identifying the current user session.
            targeting: An array of tuples specifying name/value pairs for targeting
        """
        targeting = targeting or {}
        params = {
            'key': self.api_key,
            'format': self.fmt,
            'adUnit': ad_unit,
            'targeting': json.dumps(targeting)
        }

        url = self.endpoint + "/fetch"
        response = self.http.post(url, params=params, data={})
        if response.status_code == 200:
            body = response.json()
            media = body['media'] if 'media' in body else []
            payload = body['payload'] if 'payload' in body else None

            logger.info("Received payload: " + payload)

            for m in media:
                uri = self._upload_media(m['file_url'],
                                         thumbnail_url=m['thumbnail_url'],
                                         content_description=m['content_description'])
                if not uri:
                    logger.error('Failed to upload media file.')
                    return {}

                payload = payload.replace(m['file_url'], uri)

            return self._deliver_payload(msisdn, uuid.uuid4(), payload)

        return False

    def _deliver_payload(self, msisdn, message_id, payload):
        url = self.rbm_endpoint + "/v1/phones/{0}/agentMessages?messageId={1}".format(msisdn, message_id)

        logger.info("Posting agent message {0} for {1}".format(message_id, msisdn))
        logger.info("  url = " + url)
        logger.info("  payload = " + payload)

        response = self.rbm_http.post(url, data=payload, headers={'Content-Type': 'application/json'})

        logger.info("Received response from " + url)
        logger.info("  status_code: " + str(response.status_code))
        logger.info("  response: " + json.dumps(response.json()))

        success = response.status_code == 200
        if not success:
            logger.error("Post of agent message failed!")

        return success

    def _upload_media(self, file_url, thumbnail_url=None, content_description=None):
        url = self.rbm_endpoint + "/v1/files"
        request = {'fileUrl': file_url}
        if thumbnail_url is not None:
            request['thumbnailUrl'] = thumbnail_url
        if content_description is not None:
            request['contentDescription'] = content_description

        logger.info("Uploading media file")
        logger.info("  url = " + url)
        logger.info("  fileUrl = " + file_url)
        logger.info("  thumbnailUrl = " + thumbnail_url)
        logger.info("  contentDescription = " + content_description)

        response = self.rbm_http.post(url, data=json.dumps(request), headers={'Content-Type': 'application/json'})

        logger.info("Received response from " + url)
        logger.info("  status_code: " + str(response.status_code))
        logger.info("  response: " + json.dumps(response.json()))

        success = response.status_code == 200
        if not success:
            logger.error("Post of agent message failed!")

        return response.json()['name']
