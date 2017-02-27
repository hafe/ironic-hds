==========
ironic-hds
==========

This repository contains an OpenStack Ironic driver for testing with Redfish
based system. One example is the Ericsson HDS 8000 Hyperscale Data Center
System.

Build
=====

Create a package (egg, rpm, ...) for example::

    $ python setup.py bdist_egg

Installation
============

Install the package for example::

    $ sudo easy_install ironic_hds-0.0.1.dev7-py2.7.egg

Configuration
=============

Common
++++++

Add *agent_hds* and/or *pxe_hds* to the list of *enabled_drivers* in
*/etc/ironic/ironic.conf* for example::

    enabled_drivers = pxe_ipmitool,pxe_hds,agent_hds

Restart the Ironic conductor service::

    service ironic-conductor restart


Node specific
+++++++++++++

Enroll some nodes managed by this driver::

    $ ironic node-create -d agent_hds -n hds-1 -u 4c4c4544-0053-5610-8053-b2c04f563432 \
        -i redfish_address=https://192.168.122.1:8080/redfish/v1/4c4c4544-0053-5610-8053-b2c04f563432 \
        -i redfish_username=admin \
        -i redfish_password=qwerty

Optionally allow insecure TLS connections, configure to skip certificate verification::

        -i cert_verify=false


Associate port with node created::

    $ ironic port-create -n 4c4c4544-0053-5610-8053-b2c04f563432 -a ec:f4:bb:e0:d5:dc

In the example the Redfish ComputerSystem ID is used as Ironic's node uuid.
This is not required but enables simple correlation of Ironic nodes and Redfish
ComputerSystems.

Test
====

Node introspection and overcloud deployment has been verified with the
following components:

* HW: Ericsson HDS 8000
* SW: Red Hat OpenStack 10 (Newton)

The driver can also be tested manually using ironic commands::

    $ ironic node-set-power-state hds-1 off
    $ ironic node-set-boot-device hds-1 pxe
    $ ironic node-set-power-state hds-1 on
    $ ironic node-set-boot-device hds-1 disk --persistent

Tripleo node introspection::

    $ for node in $(openstack baremetal node list --fields uuid -f value); do \
        openstack baremetal node manage $node ; done
    $ openstack overcloud node introspect --all-manageable --provide

Read out introspected node info::

    $ ironic node-show hds-1
