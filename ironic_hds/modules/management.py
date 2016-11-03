#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
HDS management interface
"""

from oslo_log import log as logging

from ironic.common import boot_devices
from ironic.conductor import task_manager
from ironic.drivers import base
from ironic_hds.modules import common

LOG = logging.getLogger(__name__)

IRONIC_TO_REDFISH_BOOT_DEVICE = {
    boot_devices.DISK: 'Hdd',
    boot_devices.PXE: 'Pxe',
    boot_devices.CDROM: 'Cd',
}

# Map Ironic boot mode name to HDS equivalent
PERSISTENT_BOOT_MODE = 'Continuous'
NON_PERSISTENT_BOOT_MODE = 'Once'


class Management(base.ManagementInterface):

    def get_properties(self):
        """Return the properties of the interface."""
        return common.COMMON_PROPERTIES

    def validate(self, task):
        """Validate the driver-specific info supplied.

        This method validates whether the 'driver_info' property of the
        supplied node contains the required information for this driver to
        manage the node.

        :param task: a TaskManager instance containing the node to act on.
        :raises: InvalidParameterValue if required driver_info attribute
                 is missing or invalid on the node.

        """
        return common.parse_driver_info(task.node)

    def get_supported_boot_devices(self, task):
        """Get a list of the supported boot devices.

        :param task: a TaskManager instance containing the node to act on.
        :returns: A list with the supported boot devices defined
                  in :mod:`ironic.common.boot_devices`.

        """
        LOG.info('get_supported_boot_devices')
        return list(IRONIC_TO_REDFISH_BOOT_DEVICE.keys())

    def get_boot_device(self, task):
        """Get the current boot device for a node.

        Returns the current boot device of the node.

        :param task: a TaskManager instance containing the node to act on.
        :raises: DracOperationError on an error from python-dracclient.
        :returns: a dictionary containing:

            :boot_device: the boot device, one of
                :mod:`ironic.common.boot_devices` or None if it is unknown.
            :persistent: whether the boot device will persist to all future
                boots or not, None if it is unknown.
        """
        client = common.get_client()
        return client.system_get_boot_source(task.node.uuid)

    @task_manager.require_exclusive_lock
    def set_boot_device(self, task, device, persistent=False):
        """Set the boot device for a node.

        Set the boot device to use on next reboot of the node.

        :param task: a TaskManager instance containing the node to act on.
        :param device: the boot device, one of
                       :mod:`ironic.common.boot_devices`.
        :param persistent: Boolean value. True if the boot device will
                           persist to all future boots, False if not.
                           Default: False.
        :raises: InvalidParameterValue if an invalid boot device is specified.
        """
        LOG.info("set_boot_device node:%s device:'%s' persistent:%s" %
                 (task.node.uuid, device, persistent))
        client = common.get_client()
        client.system_set_boot_source(task.node.uuid,
                                      IRONIC_TO_REDFISH_BOOT_DEVICE[device],
                                      "Continuous" if persistent else "Once")

    def get_sensors_data(self, task):
        """Get sensors data.

        :param task: a TaskManager instance.
        :raises: FailedToGetSensorData when getting the sensor data fails.
        :raises: FailedToParseSensorData when parsing sensor data fails.
        :returns: returns a consistent format dict of sensor data grouped by
                  sensor type, which can be processed by Ceilometer.
        """
        raise NotImplementedError()
