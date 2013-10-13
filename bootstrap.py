#!/usr/bin/python

# This program aims to start a project within the possible projects described in
# projects/*.addon

script_ver = '0.9.4'


import sys 
import os
import re
import yaml

import riclib
from riclib.debug import deb, debug_app

defaults = {
  'project_dir':  './projects/',
}

def getConfigYaml(file='config.yml'):
  """Returns a dict with configuration.

  Also provides correct messaging in case of error/
  """
  conf = {}
  try:
    yml = open("config.yml", 'r')
    whole_conf = yaml.load(yml)
    deb( whole_conf)
    conf = whole_conf['production']
    deb( conf)
  except e:
    print "Some exception: {}".format(e)
  return conf


def valid_projects(projects_dir=defaults['project_dir']):
  '''Returns a list of valid projects.

  That is taken from files: "projects/*.addon"

  '''
  project_list = []
  dirList=os.listdir(projects_dir)
  for fname in dirList:
    m = re.search('(.*)\.(bash|py)$',fname)
    if m:
      project_list.append(m.group(1))
  return project_list

def usage():
  print 'Usage: %s v%s <PROJECT_NAME>' % (sys.argv[0], script_ver)
  print 'Projects: ', ', '.join(valid_projects())
  exit(1)

def bootstrap_project(project_name, projects_dir=defaults['project_dir']):
  '''Bootstraps a project.

  For a project to be valid, it has to have

  '''
  if not(project_name in valid_projects()):
    print "Invalid project: " , project_name
    exit(2)
  deb("Valid bootstrap project: %s" % project_name)
  deb("Projects: " + ' '.join(valid_projects()) )
  bash_filename = projects_dir + project_name + ".bash"
  if os.path.exists(bash_filename):   # i.e.: 'projects/sakura.sh'
    # Execute the common before, the addon and the common after!
    os.system("PROJECT_DIR='%s' bash projects/%s.addon" % (project_name,project_name))
    print "Bash Script executed. "
  # search for python as well
  python_filename = projects_dir + project_name + ".py"
  deb("Looking for py: {}".format(python_filename))
  if os.path.exists(python_filename):   # i.e.: 'projects/sakura.py'
    deb("Great! executing python as well: {}".format(python_filename))
    os.system("python %s" % python_filename)
    print "Python Script executed. "

def main():
  deb("ARGV: {}".format(sys.argv))
  if len(sys.argv) < 2:
    usage()
  config = getConfigYaml()
  print "== Config =="
  print "Config: {}".format(config)
  print "Config.project: {}".format(config['project'])
  print "Config.bucket:  {}".format(config['bucket'])
  bootstrap_project(sys.argv[1])

main()
