"""
HDS/Redfish driver

For more information see:
https://www.dmtf.org/standards/redfish

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

"""
A cache of the power state for each system. This is because current missing
support in the redfish manager. This will be fixed in short.
Assume systems are powered ON when we start (should be safer) since the
Ironic e.g. will start by powering them on and we get to a known state.

Same for boot source, set it to disk and Ironic will change to PXE
"""
_system_power = {}
_system_boot_source = {}

RESET_TYPE_TO_POWER_STATE = {
    'On': 'On',
    'ForceOff': 'Off',
    'ForceRestart': 'On'
}


class HDSClient(object):
    """HDS client that handles the REST API
    """
    def __init__(self, api_url, username, password, cert_verify=True):
        self._api_url = api_url \
            if api_url[len(api_url) - 1] == "/" else api_url + "/"
        self._session = requests.session()
        self._session.headers["Content-Type"] = "application/json"
        self._session.auth = (username, password)
        self._session.verify = cert_verify
        self._status_forcelist = [500, 502, 503, 504]
        self._total_retries = 5
        if not cert_verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def _get(self, path):
        _logger.debug("GET " + path)
        sleeping_time = 0.1
        for i in range(self._total_retries):
            r = self._session.get(self._api_url + path, timeout=10)
            if r.status_code in self._status_forcelist:
                time.sleep(sleeping_time)
                sleeping_time *= 2
            else:
                break

        r.raise_for_status()
        data = r.json()
        _logger.debug("GET " + path + " - DONE")
        return data

    def _post(self, path, data):
        _logger.debug("POST " + path)
        sleeping_time = 0.1
        for i in range(self._total_retries):
            r = self._session.post(
                self._api_url + path, data=json.dumps(data), timeout=10)
            if r.status_code in self._status_forcelist:
                time.sleep(sleeping_time)
                sleeping_time *= 2
            else:
                break

        r.raise_for_status()
        _logger.debug("POST " + path + " - DONE")

    def _patch(self, path, data):
        _logger.debug("PATCH " + path)
        sleeping_time = 0.1
        for i in range(self._total_retries):
            r = self._session.patch(
                self._api_url + path, data=json.dumps(data), timeout=10)
            if r.status_code in self._status_forcelist:
                time.sleep(sleeping_time)
                sleeping_time *= 2
            else:
                break

        r.raise_for_status()
        _logger.debug("PATCH " + path + " - DONE")

    def system_reset(self, sys_id, reset_type):
        path = "Systems/%s" % sys_id + "/Actions/ComputerSystem.Reset"
        self._post(path, {"ResetType": reset_type})
        _system_power.update({sys_id: RESET_TYPE_TO_POWER_STATE[reset_type]})

    def system_get_power_state(self, sys_id):
        '''assumes unknown systems are powered off and remember state'''
        power_state = _system_power.get(sys_id, "On")
        _system_power.update({sys_id: power_state})
        return power_state

    def system_set_boot_source(self, sys_id, target, enabled="Once"):
        '''Sets the boot device to use on next reboot of the node.
        '''
        data = {
            "Boot": {
                "BootSourceOverrideTarget": target,
                "BootSourceOverrideEnabled": enabled
            }
        }
        self._patch("Systems/%s" % sys_id, data)
        _system_boot_source.update({sys_id: target})

    def system_get_boot_source(self, sys_id):
        '''Gets the boot device to use on next reboot of the node.
        '''
        boot_source = _system_boot_source.get(sys_id, "Disk")
        _system_boot_source.update({sys_id: boot_source})
