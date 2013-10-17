#!/usr/bin/python

import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import riclib
# from riclib import config
from riclib.gcutil_wrapper import *
from riclib.project_initiator import *


def DoSomething():
  print "nothing really"

def main():

  #######################################
  # Configuration
  #######################################
  names_and_desc = [
    ["foo", 'Server foo',  ],
    ["bar", 'Server bar, for alcoholics', ],
    ["baz", 'Lots of baz around this topic', ],
  ]
  conf = {
    'create_instances': False,
  }

  #######################################
  # Constructor
  #######################################
  p = ProjectInitiator(sys.argv[0])
  
  if conf['create_instances']:
    for hostname, description in names_and_desc:
      print("Creating normal host %s:" % (hostname) )
      # Uses default for zone, image, ...
      p.addinstance(hostname, description, tags=['test', 'deleteme'], metadata={ 'password': 'p4ssw0rd'})
    # specifies image, PD, ...
    p.addinstance('prod', 'Testing a production machine', public_ip = True, network = net, tags=['development', 'foobar'], image='centos-6' , persistent_boot_disk=True )

    # Creating a ruile which only applies to machines with tag "foobar". Imagine if it weas  Web/80 or MySQL/3306... and you can also open to just a few known IPs.
    p.addfirewall('foobar', 'Allow Mysql from target foobar', '--allowed=tcp:3306,tcp:33060 --target_tags=foobar ' )


if __name__ == "__main__":
    main()