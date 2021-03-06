#!/usr/bin/python

import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import riclib
from riclib.gcutil_wrapper import *
from riclib.project_initiator import *

version = '1.6'

def main():
  """Demonstrating Affinity in Load Balancer.

  $ gcutil help addtargetpool
  [..]
  --session_affinity: <NONE|CLIENT_IP|CLIENT_IP_PROTO>: Specifies the session affinity option for the connection. Options include:
    NONE:      connections from the same client IP may go to any VM in the target pool
    CLIENT_IP: connections from the same client IP will go to the same VM in the target pool;
    CLIENT_IP_PROTO: connections from the same client IP with the same IP protocol will go to the same VM in the targetpool.
    (default: 'NONE')

  """
  p = ProjectInitiator(sys.argv[0], run_pre_install=False) # needed also for conf :/

  #######################################
  # Configuration
  #######################################
  actions = {
     'add_machines':           True,
     'add_firewall_rules':     True,
     'add_loadbalancer_rules': True,
     'cleanup':                False,
  }
  project_name = 'torino'
  public_ip = True
  # dig +short $(hostname)
  resticted_ips = '213.155.151.238,172.26.160.3,172.28.201.4,1.2.3.4' 
  names_and_desc = [
    ["www1", 'Webserver 1 to demonstrate Load Balancing', 'red' ],
    ["www2", 'Webserver 2 to demonstrate Load Balancing', 'blue' ],
    ["www3", 'Webserver 3 to demonstrate Load Balancing', 'yellow' ],
    ["www4", 'Webserver 4 to demonstrate Load Balancing', 'green' ],
    ["www5", 'Webserver 5 to demonstrate Load Balancing', 'brown' ],
  ]
  affinities_and_nice_names = [
      ['NONE',            'none',],
      ['CLIENT_IP',       'ip'],
      ['CLIENT_IP_PROTO', 'ipproto'],
  ]
  region = p.default('region')
  prefix = p.default("vm_prefix")
  instance_names = [ prefix+host for [host,desc,whatevs] in names_and_desc] # => "prefix-web1", "prefix-web2", ..


  #######################################
  # Commands
  #######################################
  if actions['cleanup']:
    # Cleanup target pools. Pity we don't have a listtargetpools with --format names :("
    p.gcutil_cmd("""listtargetpools --filter "name eq test-lun.*bootsy.*" | fgrep "| test-" | cut -f 2 | xargs echo gcutil --project {project_id} deletetargetpool -f""".format(
      project_id=p.project_id))

  # Creates machines
  if actions['add_machines']:
    for hostname, description,color in names_and_desc:
      p.addinstance(hostname, description, 
        public_ip = public_ip,
        tags=['affinity-test'], 
        metadata={
          'gclb-affinity': 'of some kind (depends on TP/FR)',
          'bgcolor': color, # this goes into the Apache code
        },
      )

  # Plays with firewalls
  if actions['add_loadbalancer_rules']:
    # GCLB: Helth Check
    p.gcutil_cmd('addhttphealthcheck basic-check  --description="Simplest ever"') # checks for port 80
    p.gcutil_cmd('addhttphealthcheck slash-index2 --description="Cheking just port 80 for index2.html" --request_path=/index2.html')
    
    # GCLB: Target Pools
    commasep_instances_list = ','.join(instance_names)
    health_checks=[ 'basic-check', ]
    for affinity,aff_name in affinities_and_nice_names:
      targetpool = "{prefix}tp-aff{aff_name}".format(prefix=prefix, aff_name=aff_name)
      # GCLB: Adds 3 Target Pools, one for every
      ret = p.gcutil_cmd("addtargetpool {targetpool} --region {region} \
                   --zone={zone} --description 'TP with affinity: {affinity}'  --health_checks='{health_checks}' \
                   --instances='{instances_list}' --session_affinity={affinity}".format(
                      region=region, prefix=prefix,
                      instances_list=commasep_instances_list,
                      zone=p.default('zone'),
                      affinity=affinity,
                      aff_name=aff_name,
                      targetpool=targetpool,
                      health_checks=','.join(health_checks)
                      )
      )
      print "This FwdRule should only do if previous RET worked. ret=",ret
      # GCLB: 3 Forwarding Rules
      p.addforwardingrule(
          '{prefix}-fr-aff_{aff_name}'.format(prefix=prefix, aff_name=aff_name), 
          target="{targetpool}".format(targetpool=targetpool),
      )

    # GCLB: Explicitly adds instances to the TP (in case you need it)
    #p.gcutil_cmd("addtargetpoolinstance {prefix}bootsy-aff-ip --instances {instances}".format(instances=','.join(instance_names), prefix=prefix))

  if actions['add_firewall_rules']:
    # Firewalls
    p.addfirewall('bootsy-http-all',        'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=affinity-test' )
    p.addfirewall('bootsy-http-restricted', 'Allow HTTP from google IPs', '--allowed=tcp:80,tcp:443 --target_tags=www --allowed_ip_sources={}'.format(resticted_ips))


if __name__ == "__main__":
  main()
