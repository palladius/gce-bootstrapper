#!/usr/bin/python

import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import riclib
from riclib.gcutil_wrapper import *
from riclib.project_initiator import *

version = '1.4'

def main():
  """Demonstrating Affinity.


  $ gcutil help addtargetpool
  [..]
  --session_affinity: <NONE|CLIENT_IP|CLIENT_IP_PROTO>: Specifies the session affinity option for the connection. Options include:
    NONE: connections from the same client IP may go to any VM in the target pool
    CLIENT_IP: connections from the same client IP will go to the same VM in the target pool;
    CLIENT_IP_PROTO: connections from the same client IP with the same IP protocol will go to the same VM in the targetpool.
    (default: 'NONE')


  """
  p = ProjectInitiator(sys.argv[0]) # needed also for conf :/

  #######################################
  # Configuration
  #######################################
  public_ip = True
  # dig +short $(hostname)
  resticted_ips = '213.155.151.238,172.26.160.3,172.28.201.4,1.2.3.4'  
  names_and_desc = [
    ["web1", 'Webserver 1 to demonstrate Load Balancing' ],
    ["web2", 'Webserver 2 to demonstrate Load Balancing' ],
    ["web3", 'Webserver 3 to demonstrate Load Balancing' ],
    ["web4", 'Webserver 4 to demonstrate Load Balancing' ],
  ]
  region = p.default('region')
  prefix = p.default("vm_prefix")
  instance_names = [ prefix+host for [host,desc] in names_and_desc] # => "prefix-web1", "prefix-web2", ..


  #######################################
  # Commands
  #######################################
  # Creating Target Pools
  p.gcutil_cmd("addtargetpool {prefix}bootsy-tp-aff-no    --region {region} --description 'TP affinity: None'  --session_affinity NONE".format(region=region, prefix=prefix))
  p.gcutil_cmd("addtargetpool {prefix}bootsy-tp-aff-ip    --region {region} --description 'TP affinity: IP'    --session_affinity CLIENT_IP".format(region=region, prefix=prefix))
  p.gcutil_cmd("addtargetpool {prefix}bootsy-tp-aff-proto --region {region} --description 'TP affinity: Proto' --session_affinity CLIENT_IP_PROTO".format(region=region, prefix=prefix))
  

  for hostname, description in names_and_desc:
    p.addinstance(hostname, description, public_ip = public_ip, tags=['affinity-ip'], metadata={'gclb-affinity': 'ip'})
  # p.addinstance('prod', 'Testing a production machine', public_ip = public_ip, network = 'unartra', tags=['prod', 'gclb-fw'], image='centos-6' , persistent_boot_disk=True )

  # GCLB stuff
  p.addforwardingrule('bootsy-fr-aff-no', target="{prefix}bootsy-tp-aff-no".format(prefix=prefix))
  #p.addforwardingrule('bootsy-fr-aff-ip') # , extra="--target=gclb-no-affinity")
  #p.addforwardingrule('bootsy-fr-aff-proto') # , extra="--target=gclb-no-affinity")
  p.gcutil_cmd("addtargetpoolinstance bootsy-aff-ip --instances {instances}".format(
    instances=','.join(instance_names),
    )
  )

  # Firewalls
  p.addfirewall('bootsy-http-all',        'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=gclb-fw' )
  p.addfirewall('bootsy-http-restricted', 'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=gclb-fw --allowed_ip_sources={}'.format(resticted_ips))


if __name__ == "__main__":
  main()
