#!/usr/bin/python

import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import riclib
# from riclib import config
from riclib.gcutil_wrapper import *
from riclib.project_initiator import *


def main():
  #######################################
  # Configuration
  #######################################
  names_desc_opts = [
    ["debian", 'Test Debian', {'image': 'debian-7', 'tags': 'pingable,mysqlable', } ],
    ["centos", 'Test CentOS', {'image': 'centos'  , 'tags': 'apache',         } ],
  ]
  conf = {
    'create_instances': False,
    'create_firewalls': True,
  }

  #######################################
  # Constructor
  #######################################
  p = ProjectInitiator(sys.argv[0])
  
  if conf['create_instances']:
    for hostname, description, opts in names_desc_opts:
      print("Creating normal host %s:" % (hostname) )
      # Uses default for zone, image, ...
      p.addinstance(hostname, description, tags=['test', 'deleteme'], metadata={ 'password': 'p4ssw0rd'}, image=opts['image'])
    # specifies image, PD, ...
    #p.addinstance('prod', 'Testing a production machine', public_ip = True, network = net, tags=['development', 'foobar'], image='centos-6' , persistent_boot_disk=True )

  if conf['create_firewalls']:
    # Creating a ruile which only applies to machines with tag "foobar". Imagine if it weas  Web/80 or MySQL/3306... and you can also open to just a few known IPs.
    p.addfirewall('allow-mysql', 'Allow Mysql from VMs targeted mysqlable',  allowed='tcp:3306,udp:3306',        target_tags='mysqlable', )
    p.addfirewall('allow-web',   'Allow Web traffic from webbable machines', allowed='tcp:80,tcp:443,udp:12345', target_tags='webbable',  )
    p.addfirewall('allow-icmp',  'Allow ICMP for only pingable machines',    allowed='icmp', target_tags='pingable',  )

if __name__ == "__main__":
    main()