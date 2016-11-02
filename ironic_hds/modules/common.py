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
from ironic_hds.modules.client import HDSClient

COMMON_PROPERTIES = {}

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('root_url',
               help=_('URL where Redfish manager is available.')),
    cfg.StrOpt('username',
               help=_('Redfish username to be used.')),
    cfg.StrOpt('password',
               secret=True,
               help=_('Redfish password to be used.')),
    cfg.BoolOpt('cert_verify',
                default=False,
                help=_('Option to skip Redfish certificate verification')),
]

CONF = cfg.CONF
CONF.register_opts(opts, group='hds')


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

    return {}


def get_client():
    """Returns a new Redfish client object.

    :param node: an ironic node object.
    :returns: a hdsConnection object.
    :raises: InvalidParameterValue if mandatory information is missing on the
             node or on invalid input.
    """
    return HDSClient(CONF.hds.root_url,
                     CONF.hds.username,
                     CONF.hds.password,
                     CONF.hds.cert_verify)
