==========
ironic-hds
==========

This repository contains an OpenStack Ironic driver for testing with Redfish
based system. One example is the Ericsson HDS 8000 Hyperscale Data Center
System.

Build
=====

Create an RPM package suitable for RHEL/CentOS based systems::

    $ python setup.py sdist
    $ tar xvfz dist/ironic-hds-<VERSION>.tar.gz --directory /tmp
    $ cd /tmp/ironic-hds-<VERSION>
    $ python setup.py bdist_rpm

RPM should be found in the *dist* directory.

Installation
============

Install the package in the undercloud::

    $ sudo yum install ironic-hds-<VERSION>.noarch.rpm

Configuration
=============

Common
++++++

Add *pxe_hds* to the list of *enabled_drivers* in */etc/ironic/ironic.conf*

Restart the Ironic conductor service::

    sudo systemctl restart openstack-ironic-conductor

Node specific
+++++++++++++

Enroll some nodes managed by this driver::

    $ ironic node-create -d agent_hds -n hds-1 -u <uuid> \
        -i redfish_address=https://192.168.122.1 \
        -i redfish_system_id=/redfish/v1/<uuid> \
        -i redfish_username=admin \
        -i redfish_password=qwerty

Optionally configure a local CA bundle::

        -i redfish_verify_ca=/etc/ssl/certs/ca-bundle.crt

Or completely skip certificate verification::

        -i redfish_verify_ca=false

Associate port with node created::

    $ ironic port-create -n <uuid> -a <MAC address>

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
