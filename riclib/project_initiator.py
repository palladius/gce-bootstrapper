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
from util import red, deb

class ProjectInitiator:
  """This class is called when a Project has to be bootstrapped"""
  version = "1.1"

  def __init__(self, filename, conf=None, run_pre_install=True, run_post_install=True):
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
    self.project    = self.config['project_id']
    self.id = self.config['project_id'] # alias for readability

    # to decide if it launches pre_install and post_install
    self.run_pre_install = run_pre_install
    self.run_post_install = run_post_install

    # Add metadata
    common_metadata = [
      ['program', 'bootsy'],
     # ['date', '$(data)'],
      ['environment', 'prod'],
      ['addon', self.addon],
      ['bucket', self.config['bucket']],
      ['vm_prefix', self.default('vm_prefix')],

      ['admin_email', self.config['admin']['email']],
      ['admin_name',  self.config['admin']['name']],
      ['admin_user',  self.config['admin']['username']],
    ]
    for k,v in common_metadata:
      self.config['metadata'][k] = v

    print "ProjectInitiator.new('%s') => '%s'" % (self.project, self.config)
    if self.run_pre_install:
      self.pre_install()

  def config(self):
    return self.config

  def adddisk(self,diskname,group, zone ):
    gcutil_adddisk(self,diskname,group,zone)

  def addinstance(self, name, description, **kwargs):
    """Adds an instance. Very complicated code :/

    It would be nice here to add the "virtual instance name".
    
    """
    gcutil_addinstance(self, name, description, **kwargs)


  def addfirewall(self, name, description=None, allowed=None, target_tags=None, additional_options=''):
    '''Adds a firewall rule, additional oprtions is just a string... 
    
    ie: 
       p.addfirewall('foobar', 'Allow Mysql from target foobar', allowed='tcp:3306,tcp:33060', target_tags='mysqlable ' )
    ''' 
    return self.gcutil_cmd('''addfirewall {name} --description='{description}' --allowed='{allowed}' --target_tags="{target_tags}" {additional_options}'''.format(
              name=name,  
              allowed=allowed,
              description=description, 
              target_tags=target_tags,
              additional_options=additional_options))

  def delinstances(self, arr_of_instance_names):
    gcutil_delinstances(self, arr_of_instance_names)

  def addforwardingrule(self,rulename, target, region=None, extra=''):
    """Creates a forwarding rule.

    Beware thsat region is not 
    """
    if not region:
      region = self.default('region') # eg "europe-west1-a", slightly different from zone!
    self.gcutil_cmd("addforwardingrule {} --region={} --target='{}' {}".format(rulename, region, target, extra))

  def pre_install(self):
    '''This functions pushes into Google Storage all my per-machine init scripts.
    They are then pulled from init script...
    '''
    pyellow("= Pre installation: %s =" % self)
    pyellow("gsutil ls of your bucketdir: {}".format(self.config['bucket']))
    self.execute('gsutil ls {}'.format(self.config['bucket']), dryrun=False)
    
    # gsutil multithreaded
    cmds = [
      "touch .placeholder.gsutil",
      # TODO(ricc): if placeholder, then wait indefinitely.
      "gsutil cp riclib/scripts/include.bash {bucket}/addons/_common/include.bash", # common includes
      "gsutil cp .placeholder {bucket}/addons/{addon}/.placeholder",                # to create the "directory", remember these are objects
      "gsutil -m cp addons/{addon}.d/storage.*.sh {bucket}/addons/{addon}/",
      "rm .placeholder.gsutil",
    ]
    for cmd in cmds:
      self.execute(cmd.format(
          addon=self.addon,
          bucket=self.config['bucket'],
          ), 
        dryrun=False) # always a good action to do...
    self.execute('''gcutil --project={} addfirewall httpy --description="Incoming http on port 80 allowed in python lib" --allowed="tcp:http"'''.format(self.id))

  def post_install(self):
    """Put here any post-cereation code."""
    pass

  def dryrun(self):
    return self.config['dryrun']

  def default(self, mykey):
    """Returns the default value for a key.

    That's taken from configuration under 'defaults' dict.
    """
    if mykey == 'region':
      zone = self.default('zone')                       # eg "europe-west1-a"
      region = zone[:-2]                                # eg "europe-west1"
      return region

    # general catch all
    if mykey not in self.config['defaults'].keys():
      print "FATAL: key '{}' not found in config.defaults:\n{}".format(mykey, self.config )
      exit(100)
    return self.config['defaults'][mykey]

  def metadata(self):
    return self.config['metadata']

  def gcutil_cmd(self,subcommand):
    self.execute('gcutil --project {} {}'.format(self.id,subcommand))
    ret = self.execute('echo ret=$? for: subcommand')

  def __repr__(self):
    return "ProjectInitiator('{}', id='{}')".format(self.name, self.project_id)

  def __del__(self):
    """Should be the destructor."""
    deb("+ ProjectInitiator Destructor: {}".format(self))
    if self.post_install:
      self.post_install()

  def execute(self, cmd, dryrun=None):
    """Wrapper to execute code.
    """
    if dryrun is None:
      dryrun = self.dryrun()
    deb("Project Executing code (dryrun={}): '''{}'''".format(dryrun, cmd))
    if dryrun:
      print "#DRYRUN# Wont execute this: '''{}'''".format(cmd)
      return "None(_DRYRUN_)"
    else:
        deb("PWARNING, executing: {}".format(cmd))
        ret = os.system(cmd)
        print "[PCMD] return={}".format(ret)
        return ret
    return None