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

    # Add metadata
    common_metadata = [
      ['program', 'bootsy'],
     # ['date', '$(data)'],
      ['environment', 'prod'],
      ['addon', self.addon],
      ['bucket', self.config['bucket']],
      ['admin_email', self.config['admin']['email']],
      ['admin_user', self.config['admin']['username']],
      ['vm_prefix', self.default('vm_prefix')],
    ]
    for k,v in common_metadata:
      self.config['metadata'][k] = v

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

  # def setcommoninstancemetadata(self,arr_keys_values):
  #   """Gets an array of metadata, puts them into self.metadata."""
  #   for 
  #   gcutil_setcommoninstancemetadata(self, arr_keys_values)

  def addforwardingrule(self,rulename, region=None, extra=''):
    """Creates a forwarding rule.
    """
    if not region:
      region = self.default('zone')
    self.execute("gcutil --project={} addforwardingrule {} --region={} {}".format(self.project_id, rulename, region, extra))

  def pre_install(self):
    '''This functions pushes into Google Storage all my per-machine init scripts.
    They are then pulled from init script...
    '''
    pyellow( "Doing some pre installation tasks..")
    # self.setcommoninstancemetadata([
    #   ['program', 'bootsy'],
    #  # ['date', '$(data)'],
    #   ['environment', 'prod'],
    #   ['addon', self.addon],
    #   ['admin_email', self.config['admin']['email']],
    #   ['admin_user', self.config['admin']['username']],
    #   ['vm_prefix', self.default('vm_prefix')],
    # ])
    pyellow("gsutil ls of your bucketdir: {}".format(self.config['bucket']))
    self.execute('gsutil ls {}'.format(self.config['bucket']), dryrun=False)
    
    # from gcutil_wrapper  
    pyellow("Pre installation: %s" % self)
    # Opening port 80.
    #ptitle("gsutil-pushing hosts scripts for {}".format(self.addon()))
    # gsutil multithreaded
    cmds = [
      "touch .placeholder.gsutil",
      "gsutil cp riclib/scripts/include.bash {bucket}/addons/_common/include.bash",
      "gsutil cp .placeholder {bucket}/addons/{addon}/.placeholder",
      "gsutil -m cp addons/{addon}.d/host.*.sh {bucket}/addons/{addon}/",
      "rm .placeholder.gsutil",
    ]
    for cmd in cmds:
      # pyellow("Executing DEB: "+cmd)
      self.execute(cmd.format(
          addon=self.addon,
          bucket=self.config['bucket'],
          ), 
        dryrun=False) # always a good action to do...
    self.execute('''gcutil --project={} addfirewall httpy --description="Incoming http on port 80 allowed in python lib" --allowed="tcp:http"'''.format(self.id))


  def post_install(self):
    """Doing some post installation tasks.."""
    pyellow("{}: Post install".format(self))
    # requires boot script version 1.2.13 or more:
    # if there is a www host it pseudo puppetizes it :)
    #self.gcutil_cmd('push www projects/{}.d/host.*.sh /var/www/boot/'.format(self.addon))
    # the dir /var/www/'USERNAME' has been already created/rightowned with the init script :)
    #for host in ['www']:
    #  self.gcutil_cmd('push {} ./var/gcutil-*txt ./var/gcutil-*json /var/www/{}/'.format(
    #      host, self.config['admin']['username'])) # push project stuff there
    

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

  def execute(self, cmd, dryrun=None):
    """Wrapper to execute code.
    """
    if dryrun is None:
      dryrun = self.dryrun()
    self.deb("Project Executing code (dryrun={}): '''{}'''".format(dryrun, cmd))
    if dryrun:
      print "#DRYRUN# Wont execute this: '''{}'''".format(cmd)
    else:
        deb("PWARNING, executing: {}".format(cmd))
        ret = os.system(cmd)
        print "[PCMD] return={}".format(ret)