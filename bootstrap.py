#!/usr/bin/python

# This program aims to start a project within the possible projects described in
# projects/*.addon

script_ver = '0.9.4'


import sys 
import os
import re

import riclib
from riclib.util import deb, debug_app, yellow

defaults = {
  'addon_dir':  './addons/',
  'yaml_file':  'config.yml',
}


def valid_projects(addons_dir=defaults['addon_dir']):
  '''Returns a list of valid projects.

  That is taken from files: "projects/*.addon"

  '''
  project_list = []
  dirList=os.listdir(addons_dir)
  for fname in dirList:
    m = re.search('(.*)\.(bash|py)$',fname)
    if m:
      project_list.append(m.group(1))
  return project_list

def usage():
  print 'Usage: %s v%s <ADDON_NAME>' % (sys.argv[0], script_ver)
  print 'Addons: ', yellow(' '.join(valid_projects()))
  exit(1)

def bootstrap_project(addon, config, addons_dir=defaults['addon_dir']):
  '''Bootstraps a project.

  For a project to be valid, it has to have

  '''
  if not(addon in valid_projects()):
    print "Invalid project: " , addon
    exit(2)
  deb("Valid bootstrap project: %s" % addon)
  deb("Project Dir: %s" % addons_dir)
  deb("Projects: " + ', '.join(valid_projects()) )
  bash_filename = addons_dir + addon + ".bash"
  if os.path.exists(bash_filename):   # i.e.: 'projects/sakura.sh'
    # Execute the common before, the addon and the common after!
    os.system("addon_dir='%s' bash addon/%s.addon" % (addon,addon))
    print "Bash Script executed. "
  # search for python as well
  python_filename = addons_dir + addon + ".py"
  deb("Looking for py: {}".format(python_filename))
  if os.path.exists(python_filename):   # i.e.: 'projects/sakura.py'
    deb("Great! executing python as well: {}".format(python_filename))
    ret = os.system("python %s" % python_filename)
    print "Python Script executed. ret={}".format(ret)

def main():
  deb("ARGV: {}".format(sys.argv))
  if len(sys.argv) < 2:
    usage()
  config = riclib.configurator.getConfigYaml(defaults['yaml_file'])
  print "== Config =="
  print "Config: {}".format(config)
  print "Config.project: {}".format(config['project_id'])
  print "Config.bucket:  {}".format(config['bucket'])
  bootstrap_project(sys.argv[1], config)

main()
