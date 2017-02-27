"""
Helper HTTP client with retries and logging
"""

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time

try:
    from oslo_log import log as logging
except ImportError:
    import logging

_logger = logging.getLogger(__name__)


class HTTPClient(object):
    """HTTP client
    """
    def __init__(self, username, password, cert_verify=True):
        self._session = requests.session()
        self._session.headers["Content-Type"] = "application/json"
        self._session.auth = (username, password)
        self._session.verify = cert_verify
        self._status_forcelist = [500, 502, 503, 504]
        self._total_retries = 5
        if not cert_verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def get(self, url):
        _logger.debug("GET " + url)
        sleeping_time = 0.1
        for i in range(self._total_retries):
            r = self._session.get(url, timeout=10)
            if r.status_code in self._status_forcelist:
                time.sleep(sleeping_time)
                sleeping_time *= 2
            else:
                break

        r.raise_for_status()
        data = r.json()
        _logger.debug("GET " + url + " - DONE")
        return data

    def post(self, url, data):
        _logger.debug("POST " + url)
        sleeping_time = 0.1
        for i in range(self._total_retries):
            r = self._session.post(url, data=json.dumps(data), timeout=10)
            if r.status_code in self._status_forcelist:
                time.sleep(sleeping_time)
                sleeping_time *= 2
            else:
                break

        r.raise_for_status()
        _logger.debug("POST " + url + " - DONE")

    def patch(self, url, data):
        _logger.debug("PATCH " + url)
        sleeping_time = 0.1
        for i in range(self._total_retries):
            r = self._session.patch(url, data=json.dumps(data), timeout=10)
            if r.status_code in self._status_forcelist:
                time.sleep(sleeping_time)
                sleeping_time *= 2
            else:
                break

        r.raise_for_status()
        _logger.debug("PATCH " + url + " - DONE")
