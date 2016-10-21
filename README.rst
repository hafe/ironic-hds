ironic-hds
==========
This repository contains a temporary OpenStack Ironic driver for testing with Redfish based system.
One example is the Ericsson HDS system.

Installation
============

Create a tar of the drivers directory:
$ tar cvfz ~/aball.tgz drivers

Transfer tar ball to system where Ironic is installed.
Untar the ball standing in the proper directory:

$ cd /usr/lib/python2.7/site-packages/ironic

$ tar xvfz ~/aball.tgz

Configuration
=============

Add something similar to this in /etc/ironic/ironic.conf:

enabled_drivers=agent_hds,...

[hds]
root_url=http://192.168.122.1:8080/redfish/v1/

username=admin

password=qwerty


And a bit hackish, edit the original python egg's entrypoints:

$ sudo vi /usr/lib/python2.7/site-packages/ironic-5.1.2-py2.7.egg-info/entry_points.txt

And add:

agent_hds = ironic.drivers.hds:AgentHDSDriver

in the [ironic.drivers] section

Enroll some nodes managed by this driver:

$ ironic node-create -d agent_hds -n hds-1 -u 4c4c4544-0053-5610-8053-b2c04f563432

Test
====

So far just tested with a redfish simulator as backend and using ironic commands:

$ ironic node-power-state-set hds-1 off

$ ironic node-set-boot-device hds-1 pxe

$ ironic node-power-state-set hds-1 on

$ ironic node-set-boot-device hds-1 disk --persistent

Check the conductor log file and read out the node info:

$ ironic node-show hds-1

