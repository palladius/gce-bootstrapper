
from gcutil_wrapper import *

class ProjectInitiator:
  """This class is called when a Project has to be bootstrapped"""
  project = None
  config = { 'foo': 'configurator'}

  def __init__(self, filename, config):
    self.data = []
    self.project = autodetect_project(filename)
    self.config = config
    print "ProjectInitiator.new('%s') => '%s'" % (filename, self.project)
    print " + Config: {}".format(config)
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

