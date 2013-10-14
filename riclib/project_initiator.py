"""This is a ProjectInitiator class.


It provides utilities to call gcutil in a pythonic way.

TODO(ricc): move all gcutil commands from gcutil_wrapper to here. I started with addforwardingrule
            and it works pretty well. Ideally, move gcutil_addinstance, the rest is easy.
"""


from gcutil_wrapper import *

import re
import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from riclib import configurator
from configurator import getConfigYaml

class ProjectInitiator:
  """This class is called when a Project has to be bootstrapped"""
  project = None
  config = {}

  def __init__(self, filename, conf=None):
    """Takes a filename which becomes the addon.

    Addon can be: "lamp", "load-balancer", ...

    """
    addon = os.path.basename(filename)
    if re.search(".*\.(py|sh)$", addon):
      addon = addon[:-3]                       # removing the ".py" or ".sh" extension..
    self.name = addon
    self.addon = addon
    self.config = conf if conf else getConfigYaml()
    self.project_id = self.config['project_id']
    self.id = self.config['project_id'] # alias for readability
    print "ProjectInitiator.new('%s') => '%s'" % (self.project, self.config)
    self.pre_install()

  def deb(self, s):
    '''Colored Debug function'''
    if len(s) > 0 and self.config['debug']:
      print "\033[1;30m#PEB# {}\033[0m".format(s)

  def config(self):
    return self.config

  def adddisk(self,diskname,group, zone ):
    gcutil_adddisk(self,diskname,group,zone)

  def addinstance(self, name, description, **kwargs):
    gcutil_addinstance(self, name, description, **kwargs)

  def addfirewall(self, name, description, args):
    gcutil_addfirewall(self, name, description, args)

  def delinstances(self, arr_of_instance_names):
    gcutil_delinstances(self, arr_of_instance_names)

  def setcommoninstancemetadata(self,arr_keys_values):
    gcutil_setcommoninstancemetadata(self, arr_keys_values)

  def addforwardingrule(self,rulename, region=None, extra=''):
    """Creates a forwarding rule.
    """
    if not region:
      region = self.default('zone')
    self.execute("gcutil --project={} addforwardingrule {} --region={} {}".format(self.project_id, rulename, region, extra))

  def pre_install(self):
    print "Doing some pre installation tasks.."
    self.setcommoninstancemetadata([
      ['owner', 'riccardo'],
      ['data', '$(data)'],
      ['environment', 'test'],
    ])

  def post_install(self):
    """Doing some post installation tasks.."""
    pyellow("{}: Post installation".format(self))
    # requires boot script version 1.2.13 or more:
    # if there is a www host it pseudo puppetizes it :)
    self.gcutil_cmd('push www projects/{}.d/host.*.sh /var/www/boot/'.format(self.addon))
    # the dir /var/www/'USERNAME' has been already created/rightowned with the init script :)
    for host in ['www']:
      self.gcutil_cmd('push {} ./var/gcutil-*txt ./var/gcutil-*json /var/www/{}/'.format(
          host, self.config['admin']['username'])) # push project stuff there
    

  def dryrun(self):
    return self.config['dryrun']

  def default(self, mykey):
    """Returns the default value for a key.

    That's taken from configuration under 'defaults' dict.
    """
    if mykey not in self.config['defaults'].keys():
      print "FATAL: key '{}' not found in config.defaults:\n{}".format(mykey, self.config )
      exit(100)
    return self.config['defaults'][mykey]

  def metadata(self):
    return self.config['metadata']

  def gcutil_cmd(self,subcommand):
    self.execute('gcutil --project {} {}'.format(self.id,subcommand))

  def __repr__(self):
    return "ProjectInitiator('{}', id='{}')".format(self.name, self.project_id)

  def __del__(self):
    """Should be the destructor."""
    self.deb("+ ProjectInitiator Destructor: {}".format(self))
    self.post_install()

  def execute(self, cmd):
    """Wrapper to execute code.
    """
    self.deb("Project Executing code (dryrun={}): '''{}'''".format(self.dryrun(), cmd))
    if self.dryrun():
      print "#DRYRUN# Wont execute this: '''{}'''".format(cmd)
    else:
        deb("PWARNING, executing: {}".format(cmd))
        ret = os.system(cmd)
        print "[PCMD] return={}".format(ret)