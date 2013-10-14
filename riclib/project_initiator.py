"""This is a ProjectInitiator class.


It provides utilities to call gcutil in a pythonic way.

TODO(ricc): move all gcutil commands from gcutil_wrapper to here. I started with addforwardingrule
            and it works pretty well. Ideally, move gcutil_addinstance, the rest is easy.
"""


from gcutil_wrapper import *

import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from riclib import configurator
from configurator import getConfigYaml

class ProjectInitiator:
  """This class is called when a Project has to be bootstrapped"""
  project = None
  config = { 'foo': 'configurator'}

  def __init__(self, filename, conf=None):
    self.name = os.path.basename(filename)[:-3] # removing the ".py" extension..
    self.config = conf if conf else getConfigYaml()
    self.project_id = self.config['project_id']
    self.id = self.config['project_id'] # alias for readability
    print "ProjectInitiator.new('%s') => '%s'" % (self.project, self.config)
    self.pre_install()

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
    print "Post install tasks"
    gcutil_wrapper.common_post()

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

  def __repr__(self):
    return "ProjectInitiator('{}', id='{}')".format(self.name, self.project_id)

  def __del__(self):
    """Should be the destructor."""
    deb("+ ProjectInitiator Destructor: {}".format(self))
    self.post_install()

  def execute(self, cmd):
    """Wrapper to execute code.
    """
    deb("Project Executing code (dryrun={}): '''{}'''".format(self.dryrun(), cmd))
    if self.dryrun():
      print "#DRYRUN# Wont execute this: '''{}'''".format(cmd)
    else:
        deb("PWARNING, executing: {}".format(cmd))
        ret = os.system(cmd)
        print "[PCMD] return={}".format(ret)