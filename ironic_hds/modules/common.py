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

from oslo_config import cfg
from oslo_log import log as logging
from ironic.common.i18n import _
from ironic.drivers.modules import deploy_utils

COMMON_PROPERTIES = {}

LOG = logging.getLogger(__name__)

REQUIRED_PROPERTIES = {
    'redfish_uri': _('Redfish System URI. Required.'),
    'redfish_username': _('Redfish Manager admin/server-profile username. Required.'),
    'redfish_password': _('Redfish Manager password. Required.'),
}

OPTIONAL_PROPERTIES = {
    'redfish_verify_ca': _("True/False/Cert. Optional."),
}

COMMON_PROPERTIES = {}
COMMON_PROPERTIES.update(REQUIRED_PROPERTIES)
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

    info = {}
    for param in REQUIRED_PROPERTIES:
        info[param] = node.driver_info.get(param)
    error_msg = (_("%s driver requires these parameters to be set in the "
                   "node's driver_info.") %
                 node.driver)
    deploy_utils.check_for_missing_params(info, error_msg)
    return info
