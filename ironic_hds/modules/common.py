#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Common functionality shared between different modules.
"""

import os

from oslo_config import cfg
from oslo_log import log as logging
from ironic.common.i18n import _
from ironic.drivers.modules import deploy_utils

COMMON_PROPERTIES = {}

LOG = logging.getLogger(__name__)

REQUIRED_PROPERTIES = {
    'redfish_address': _('The URL address to the Redfish controller. It '
                         'should include scheme and authority portion of '
                         'the URL. For example: https://mgmt.vendor.com. '
                         'Required'),
    'redfish_system_id': _('The canonical path to the ComputerSystem '
                           'resource that the driver will interact with. '
                           'It should include the root service, version and '
                           'the unique resource path to a ComputerSystem '
                           'within the same authority as the redfish_address '
                           'property. For example: /redfish/v1/Systems/1. '
                           'Required')
}

OPTIONAL_PROPERTIES = {
    'redfish_username': _('User account with admin/server-profile access '
                          'privilege. Although this property is not '
                          'mandatory it\'s highly recommended to set a '
                          'username. Optional'),
    'redfish_password': _('User account password. Although this property is '
                          'not mandatory, it\'s highly recommended to set a '
                          'password. Optional'),
    'redfish_verify_ca': _('Either a boolean value, a path to a CA_BUNDLE '
                           'file or directory with certificates of trusted '
                           'CAs. If set to True the driver will verify the '
                           'host certificates; if False the driver will '
                           'ignore verifying the SSL certificate; if it\'s '
                           'a path the driver will use the specified '
                           'certificate or one of the certificates in the '
                           'directory. Defaults to True. Optional')
}

COMMON_PROPERTIES = REQUIRED_PROPERTIES.copy()
COMMON_PROPERTIES.update(OPTIONAL_PROPERTIES)


def parse_driver_info(node):
    """Parse a node's driver_info values.

    Parses the driver_info of the node, reads default values
    and returns a dict containing the combination of both.

    :param node: an ironic node object.
    :returns: a dict containing information from driver_info
              and default values.
    :raises: InvalidParameterValue if some mandatory information
             is missing on the node or on invalid inputs.
    """

    driver_info = node.driver_info or {}
    for param in REQUIRED_PROPERTIES:
        driver_info[param] = node.driver_info.get(param)
    error_msg = (_("%s driver requires these parameters to be set in the "
                   "node's driver_info.") %
                 node.driver)
    deploy_utils.check_for_missing_params(driver_info, error_msg)

    # Check if verify_ca is a boolean or a file/directory in the file-system
    verify_ca = driver_info.get('redfish_verify_ca', True)
    if not isinstance(verify_ca, bool):
        if not os.path.exists(verify_ca):
            raise ValueError(
                _('Invalid value "%(value)s given to '
                  'driver_info/redfish_verify_ca on node %(node)s. '
                  'The value should be either a boolean, a path to a '
                  'CA_BUNDLE file or directory with certificates of '
                  'trusted CAs') % {'value': verify_ca, 'node': node.uuid})

    return driver_info
