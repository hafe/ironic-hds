ironic-hds
==========
This repository contains a temporary OpenStack Ironic driver for testing with Redfish based system.
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

enabled_drivers=agent_hds,...

[hds]

root_url=https://192.168.122.1:8080/redfish/v1/

username=admin

password=qwerty


Enroll some nodes managed by this driver:

$ ironic node-create -d agent_hds -n hds-1 -u 4c4c4544-0053-5610-8053-b2c04f563432

Currently Ironic's node uuid is used as a Redfish ComputerSystem ID. This is perhaps
not proper Redfish but plays with HDS and no extra configuration is needed.

Test
====

So far just tested with a redfish simulator as backend and using ironic commands:

$ ironic node-power-state-set hds-1 off

$ ironic node-set-boot-device hds-1 pxe

$ ironic node-power-state-set hds-1 on

$ ironic node-set-boot-device hds-1 disk --persistent

Check the conductor log file and read out the node info:

$ ironic node-show hds-1

