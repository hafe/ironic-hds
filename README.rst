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

Add something similar to this in /etc/ironic/ironic.conf:

enabled_drivers=pxe_hds,...

[hds]

root_url=https://192.168.122.1:8080/redfish/v1/

username=admin

password=qwerty

#cert_verify=false

Enroll some nodes managed by this driver::

    $ ironic node-create -d agent_hds -n hds-1 -u 4c4c4544-0053-5610-8053-b2c04f563432
    $ ironic port-create -n 4c4c4544-0053-5610-8053-b2c04f563432 -a ec:f4:bb:e0:d5:dc

Currently Ironic's node uuid is used as a Redfish ComputerSystem ID. This is
perhaps not proper Redfish but plays well with HDS and no extra configuration
is needed.

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
