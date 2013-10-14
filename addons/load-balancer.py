#!/usr/bin/python

import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import riclib
from riclib.gcutil_wrapper import *
from riclib.project_initiator import *


def main():

  #######################################
  # Configuration
  #######################################
  public_ip = True
  #zones  = ["us-central1-a", "us-east1-a", "europe-west1-a", "europe-west1-b"]
  # dig +short $(hostname)
  resticted_ips = '213.155.151.238,172.26.160.3,172.28.201.4'  
  names_and_desc = [
    ["web1", 'Webserver 1 to Demonstrate Load Balancing' ],
    ["web2", 'Webserver 2 to Demonstrate Load Balancing' ],
    ["web3", 'Webserver 3 to Demonstrate Load Balancing' ],
  ]


  #######################################
  # Commands
  #######################################
  p = ProjectInitiator(sys.argv[0])

  for hostname, description in names_and_desc:
    # pyellow("Creating normal host %s ('%s')" % (hostname, description) )
    p.addinstance(hostname, description, public_ip = public_ip, tags=['affinity-ip'], metadata={ 'gclb-affinity': 'ip'})
  p.addinstance('prod', 'Testing a production machine', public_ip = public_ip, network = 'unartra', tags=['prod'], image='centos-6' , persistent_boot_disk=True )

  p.addfirewall('goohttp', 'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=goohttp ' )
  p.addfirewall('gooderek2', 'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=goohttp --allowed_ip_sources:%s' % resticted_ips )

  p.addforwardingrule('ricc-fwd-rule', region=p.default('zone'), extra="--target=gclb-03563758-no-affinity")

if __name__ == "__main__":
  main()
