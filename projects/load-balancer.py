#!/usr/bin/python

import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import riclib
# from riclib import config
from riclib.gcutil_wrapper import *
from riclib.project_initiator import *


ric_mind_idea = '5.0' # the newest now

def main():
  #project = autodetect_project(sys.argv[0])
  # common_pre(project)
  #project.common_pre()

  #######################################
  # Configuration
  #######################################
  public = True
  zones  = ["us-central1-a", "us-east1-a", "europe-west1-a", "europe-west1-b"]
  net    = 'unartra'
  # dig +short $(hostname)
  resticted_ips = '213.155.151.238,172.26.160.3,172.28.201.4'
  dflt_zone = zones[0]
  
  names_and_desc = [
    ["web1", 'Webserver 1' ],
    ["web2", 'Webserver 2' ],
    ["web3", 'Webserver 3' ],
  ]

  #######################################
  # Commands
  #######################################
  p = ProjectInitiator(sys.argv[0])
  
  for hostname, description in names_and_desc:
    yellow("Creating normal host %s ('%s')" % (hostname, description) )
    p.addinstance(hostname, description, public_ip = True, tags=['affinity-ip'], metadata={ 'gclb-affinity': 'ip'})
  p.addinstance('prod', 'Testing a production machine', public_ip = True, network = net, tags=['prod'], image='centos-6' , persistent_boot_disk=True )

  p.addfirewall('goohttp', 'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=goohttp ' )
  p.addfirewall('gooderek2', 'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=goohttp --allowed_ip_sources:%s' % resticted_ips )

  # common_post(project)
  #project.common_post()

main()
