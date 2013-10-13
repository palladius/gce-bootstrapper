#!/usr/bin/python

# This program aims to start a project within the possible projects described in
# projects/*.addon

script_ver = '0.9.4'
projects_dir = './projects/'

import sys 
import os
import re

import riclib

from riclib.debug import deb, debug_app
  
def valid_projects():
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

def bootstrap_project(project_name):
  '''Bootstraps a project'''
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
  if os.path.exists(python_filename):   # i.e.: 'projects/sakura.py'
    print "great! executing python as well: ", python_filename
    os.system("python %s" % python_filename)
    print "Python Script executed. "

def main():
  deb("ARGV: {}".format(sys.argv))
  if len(sys.argv) < 2:
    usage()
  bootstrap_project(sys.argv[1])

main()
