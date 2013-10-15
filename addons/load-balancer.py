#!/usr/bin/python

import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import riclib
from riclib.gcutil_wrapper import *
from riclib.project_initiator import *

version = '1.5'

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
  add_firewall_rules = False
  add_machines = True
  public_ip = True
  # dig +short $(hostname)
  resticted_ips = '213.155.151.238,172.26.160.3,172.28.201.4,1.2.3.4' 
  names_and_desc = [
    ["www1", 'Webserver 1 to demonstrate Load Balancing', 'red' ],
    ["www2", 'Webserver 2 to demonstrate Load Balancing', 'blue' ],
    ["www3", 'Webserver 3 to demonstrate Load Balancing', 'yellow' ],
    ["www4", 'Webserver 4 to demonstrate Load Balancing', 'green' ],
  ]
  region = p.default('region')
  prefix = p.default("vm_prefix")
  instance_names = [ prefix+host for [host,desc,whatevs] in names_and_desc] # => "prefix-web1", "prefix-web2", ..


  #######################################
  # Commands
  #######################################

  # Creates machines
  if add_machines:
    for hostname, description,color in names_and_desc:
      p.addinstance(hostname, description, 
        public_ip = public_ip,
        tags=['affinity-ip', ], 
        metadata={
          'gclb-affinity': 'of some kind (depends on TP/FR)',
          'bgcolor': color, # this goes into the Apache code
        },
      )

  # Plays with firewalls
  if add_firewall_rules:
    # Creating Target Pools
    p.gcutil_cmd("addtargetpool {prefix}bootsy-tp-aff-no    --region {region} --description 'TP affinity: None'  --session_affinity NONE".format(region=region, prefix=prefix))
    p.gcutil_cmd("addtargetpool {prefix}bootsy-tp-aff-ip    --region {region} --description 'TP affinity: IP'    --session_affinity CLIENT_IP".format(region=region, prefix=prefix))
    p.gcutil_cmd("addtargetpool {prefix}bootsy-tp-aff-proto --region {region} --description 'TP affinity: Proto' --session_affinity CLIENT_IP_PROTO".format(region=region, prefix=prefix))

    # GCLB stuff
    p.addforwardingrule('{prefix}bootsy-fr-aff-no'.format(prefix=prefix),    target="{prefix}bootsy-tp-aff-no".format(prefix=prefix))
    p.addforwardingrule('{prefix}bootsy-fr-aff-ip'.format(prefix=prefix),    target="{prefix}bootsy-tp-aff-ip".format(prefix=prefix))
    #p.addforwardingrule('{prefix}bootsy-fr-aff-proto', target="{prefix}bootsy-tp-aff-proto".format(prefix=prefix))

    p.gcutil_cmd("addtargetpoolinstance {prefix}bootsy-aff-ip --instances {instances}".format(
      instances=','.join(instance_names),
      prefix=prefix,
      )
    )
    p.gcutil_cmd('addhttphealthcheck bootsy-check80 --description="Cheking just port 80 for index.html" --request_path=/index.html')
         # --check_interval_sec=<interval-in-secs>
         # --check_timeout_sec=<timeout-secs> \
         # --healthy_threshold=<healthy-threshold> \
         # --unhealthy_threshold=<unhealthy-threshold>
         # --host=<host> \
         # --request_path=<path>
         # --port=<port>
    # Firewalls
    p.addfirewall('bootsy-http-all',        'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=affinity-ip' )
    p.addfirewall('bootsy-http-restricted', 'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=affinity-ip --allowed_ip_sources={}'.format(
      resticted_ips))


if __name__ == "__main__":
  main()
