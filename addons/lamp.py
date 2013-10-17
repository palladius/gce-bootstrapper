#!/usr/bin/python

import sys                       
import riclib

from riclib.gcutil_wrapper import *
from riclib.project_initiator import *


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
print "cmd_folder: ", cmd_folder

#config = riclib.config.getConfigYaml(defaults['yaml_file'])


def main2():
  project = autodetect_project(sys.argv[0])
  common_pre(project)
  gcutil_delinstances(project, ['test'] )                      # recreate it all the time
  common_post(project)
 

def main():
  my_zone = 'us-central2-a' # My favorite zone. TODO read it from YML
  my_zone_a = 'us-central1-a'
  my_zone_b = 'us-central2-a'
  project = autodetect_project(sys.argv[0])
  p = ProjectInitiator(sys.argv[0])

  common_pre(project)

  public = True
  net = 'default'
  
  p.delinstances( ['test','nagios-ea'] ) # recreate it all the time
  
  p.addfirewall('http80', 'Apache port 80', '--allowed=tcp:80' )

  # Adding disks
  gcutil_adddisk(project, 'd2', )
  #gcutil_adddisk(project, 'd1', zone = "some other zone")

  # Adding instances
  gcutil_addinstance(project, "nagios-ea", "Nagios zone my_zone_a",  public_ip = True, network=net, zone = my_zone_a, disk = 'nagios-ea', tags=['lampy'])
  gcutil_addinstance(project, "nagios-eb", "Nagios zone my_zone_b",  public_ip = True, network=net, zone = my_zone_b, disk = 'nagios-eb', tags=['lampy'])

  gcutil_addinstance(project, "www", "", public_ip = True) # you always need one
  #gcutil_addinstance(project, "test", "test with four disks!", public_ip = True, disks = ['d1','d2','d3','d4'], zone = my_zone_b)

  p.addinstance('public-ror-septober', 'My RoR septober instance' , public_ip = True )
  p.addinstance('private-ricc-gloudia',  'Google Cloudia Desktop machine (personal stuff, dropbox and other linux stuff maybe X)' )

  common_post(project)

main()
