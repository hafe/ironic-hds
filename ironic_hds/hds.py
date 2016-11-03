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
Redfish Driver
"""

from ironic.drivers import base
from ironic.drivers.modules import agent
from ironic.drivers.modules import iscsi_deploy
from ironic.drivers.modules import pxe
from ironic_hds.modules import common
from ironic_hds.modules import management as hds_mgmt
from ironic_hds.modules import power as hds_power


class AgentAndHDSDriver(base.BaseDriver):
    """Agent + hds driver.

    This driver implements the `core` functionality, combining
    :class:ironic.drivers.modules.hds.power.Power for power
    on/off and reboot with
    :class:'ironic.driver.modules.agent.AgentDeploy' (for image deployment.)
    Implementations are in those respective classes;
    this class is merely the glue between them.
    """

    def __init__(self):
        self.boot = pxe.PXEBoot()
        self.deploy = agent.AgentDeploy()
        self.management = hds_mgmt.Management()
        self.power = hds_power.Power()
        self.vendor = agent.AgentVendorInterface()
        #self.inspect = inspector.Inspector.create_if_enabled('AgentHDSDriver')

        # get a client just check global driver configuration
        common.get_client()


class PXEAndHDSDriver(base.BaseDriver):
    """PXE + ISCSI + hds driver.
    """

    def __init__(self):
        self.boot = pxe.PXEBoot()
        self.deploy = iscsi_deploy.ISCSIDeploy()
        self.management = hds_mgmt.Management()
        self.power = hds_power.Power()
        self.vendor = iscsi_deploy.VendorPassthru()

        # get a client just check global driver configuration
        common.get_client()
