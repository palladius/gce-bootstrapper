
from gcutil_wrapper import *

import sys                       
import os.path
# Adds "superior" dir to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from riclib import config

class ProjectInitiator:
  """This class is called when a Project has to be bootstrapped"""
  project = None
  config = { 'foo': 'configurator'}

  def __init__(self):
    # self.data = []
    self.config = config.getConfigYaml()
    self.project = self.config['project']
    # OLD: self.project = autodetect_project(filename)
    print "ProjectInitiator.new('%s') => '%s'" % (self.project, self.config)
    self.pre_install()

  def addinstance(self, name, description, **kwargs):
    gcompute_addinstance(self.project, name, description, **kwargs)

  def addfirewall(self, name, description, args):
    gcompute_addfirewall(self.project, name, description, args)

  def delinstances(self, arr_of_instance_names):
    gcompute_delinstances(self.project, arr_of_instance_names)

  def setcommoninstancemetadata(self,arr_keys_values):
    gcompute_setcommoninstancemetadata(self.project, arr_keys_values)

  def pre_install(self):
    print "Doing some pre installation tasks.."
    self.setcommoninstancemetadata([
      ['owner', 'riccardo'],
      ['data', '$(data)'],
      ['environment', 'test'],
    ])

  def adddisk(self,diskname,group, zone ):
    gcompute_adddisk(self.project,diskname,group,zone)

