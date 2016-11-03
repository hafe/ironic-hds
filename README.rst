ironic-hds
==========
This repository contains an OpenStack Ironic driver for testing with Redfish based system.
One example is the Ericsson HDS system.

Build
=====

Create a package (egg, rpm, ...) for example:

$ python setup.py bdist_egg

Installation
============

Install the package for example:

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

Enroll some nodes managed by this driver:

$ ironic node-create -d agent_hds -n hds-1 -u 4c4c4544-0053-5610-8053-b2c04f563432

$ ironic port-create -n 4c4c4544-0053-5610-8053-b2c04f563432 -a ec:f4:bb:e0:d5:dc

Currently Ironic's node uuid is used as a Redfish ComputerSystem ID. This is perhaps
not proper Redfish but plays well with HDS and no extra configuration is needed.

Test
====

Tested with a HDS backend (Redfish manager) using ironic commands:

$ ironic node-power-state-set hds-1 off

$ ironic node-set-boot-device hds-1 pxe

$ ironic node-power-state-set hds-1 on

$ ironic node-set-boot-device hds-1 disk --persistent


Also tested with tripleo node introspection:

$ openstack baremetal introspection bulk start


Check the conductor log file and read out the node info:

$ ironic node-show hds-1

