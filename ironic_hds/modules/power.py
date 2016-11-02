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
HDS power interface
"""

from oslo_log import log as logging

from ironic.common import exception
from ironic.common.i18n import _LE
from ironic.common import states
from ironic.conductor import task_manager
from ironic.drivers import base
from ironic_hds.modules import common

LOG = logging.getLogger(__name__)

REDFISH_TO_IRONIC_POWER_STATES = {
    'On': states.POWER_ON,
    'Off': states.POWER_OFF,
    'PoweringOn': states.POWER_ON,
    'PoweringOff': states.POWER_ON,
}


class Power(base.PowerInterface):
    """Interface for power-related actions."""

    def get_properties(self):
        """Return the properties of the interface."""
        return common.COMMON_PROPERTIES

    def validate(self, task):
        """Validate the driver-specific Node power info.

        This method validates whether the 'driver_info' property of the
        supplied node contains the required information for this driver to
        manage the power state of the node.

        :param task: a TaskManager instance containing the node to act on.
        :raises: InvalidParameterValue if required driver_info attribute
                 is missing or invalid on the node.
        """
        return common.parse_driver_info(task.node)

    def get_power_state(self, task):
        """Return the power state of the task's node.

        :param task: a TaskManager instance containing the node to act on.
        :returns: the power state, one of :mod:`ironic.common.states`.
        :raises: InvalidParameterValue if required credentials are missing.
        :raises: RedfishOperationError on an error from redfish.
        """

        LOG.info('get_power_state node %s' % task.node.uuid)

        node = task.node
        client = common.get_client()

        try:
            power_state = client.system_get_power_state(node.uuid)
        except Exception as exc:
            LOG.error(_LE('HDS driver failed to get node '
                          '%(node_uuid)s power state. '
                          'Reason: %(error)s.'),
                      {'node_uuid': node.uuid, 'error': exc})
            raise

        return REDFISH_TO_IRONIC_POWER_STATES[power_state]

    @task_manager.require_exclusive_lock
    def set_power_state(self, task, power_state):
        """Set the power state of the task's node.

        :param task: a TaskManager instance containing the node to act on.
        :param power_state: a power state from :mod:`ironic.common.states`.
        :raises: RedfishOperationError on an error from redfish.
        """

        LOG.info('set_power_state node %s state "%s"' %
                 (task.node.uuid, power_state))

        node = task.node
        client = common.get_client()
        if power_state == states.POWER_ON:
            # "ForceRestart" seems to work better then "On"
            reset_type = 'ForceRestart'
        elif power_state == states.POWER_OFF:
            reset_type = 'ForceOff'
        elif power_state == states.REBOOT:
            reset_type = 'ForceRestart'
        else:
            raise ValueError(power_state)

        try:
            client.system_reset(node.uuid, reset_type)
        except Exception as exc:
            LOG.error(_LE('HDS driver failed to reset node '
                          '%(node_uuid)s to %(power_state)s. '
                          'Reason: %(error)s.'),
                      {'node_uuid': node.uuid,
                       'power_state': power_state,
                       'error': exc})
            raise

    @task_manager.require_exclusive_lock
    def reboot(self, task):
        """Perform a reboot of the task's node.

        :param task: a TaskManager instance containing the node to act on.
        :raises: InvalidParameterValue if required credentials are missing.
        :raises: RedfishOperationError on an error from redfish.
        """
        LOG.info('reboot node %s' % task.node.uuid)

        self.set_power_state(task, states.REBOOT)
