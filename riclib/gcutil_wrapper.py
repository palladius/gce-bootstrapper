
##################################################
# gcompute library
##################################################

from datetime   import datetime, date, time 
from debug      import deb
from subprocess import call

import subprocess
import os

#######################
# Todo library
#######################

lib_ver_common         = '1.0.8'


# Zone REading from                                        2012-11-01 manually edited :)
# TODO import from YAML!

# TODO take from conf
#default_tags           = [ 'ricpy', 'torino' ]
#default_zone           = 'europe-west1-b'     # Europe, yay!
#default_machine_type   = 'n1-standard-1'  # for old project its 'standard-1-cpu'
#default_network        = 'default'
#default_startup_script = './projects/riclib/scripts/common-startup-script.sh'


lib_ver_history = '''
20120924 1.0.6 pushing common.bash to /projects/common/include.bash
20120924 1.0.5 adding jason dumps to vars (to rebuild key/vals in case I break them)
201209?? 1.0.4 ???
20120727 1.0.3 adding IMAGE support
20120727 1.0.1 bugfixes
20120727 1.0.0 metadata: project2 -> project
20120726 0.9.5 auto-upload gsutil host.HOSTNAME.sh init scripts!
20120726 0.9.4 changed default machine_type...
201206?? 0.9.3 old stuff..
'''

def execute(code):
  deb("Executing: " + code)
  os.system(code) 

def gcutil_delinstance(project, name):  
  execute( """gcutil --project={} deleteinstance -f '{}'""".format(name, project) )

def gcutil_delinstances(project, names):
  for name in names:
    deb("Deleting instance: %s" % name)
    gcutil_delinstance(project, name)

#def gcutil_using_dict(mandatory_args, **opt_args):
#  opt_args["arg_name"] ||= 'dflt'

def gcutil_addfirewall(project, name, description, additional_options):
  '''Adds a firewall rule, additional oprtions is just a string... 
  
  sorry for my lazyness  
  ''' 
  command = '''gcutil addfirewall '%s' --project=%s:%s --description='[%s.py] %s' \
  %s ''' % (name, default_group,project, project, description, additional_options)
  deb(command)
  os.system(command)

def gcutil_addinstance(project, name, description, 
  public_ip = False, 
  tags = [],
  group = default_group , 
  zone  = default_zone,
  machine_type = default_machine_type,
  network = default_network,
  startup_script = default_startup_script,
  disk = None,
  disks = [] ,
  image = None,
  persistent_boot_disk = False,
  additional_options = ''
  ):
  '''Adds an instance of gcompute (for the moment using the bash script, in the future using
  directly the API written - putacaso - in python!
  '''
  if (tags.__class__ != list):
    print "Sorry, I need a list for 'tags', not a %s" % (tags.__class__)
    exit(1)
  if (disks.__class__ != list):
    print "Sorry, I need a list for 'disks', not a %s" % (tags.__class__)
    exit(1)

  # I guess it extends the tags, adding them to the default ones!
  all_tags = tags
  all_tags.extend(default_tags)
  all_tags.append("v%s" % str(lib_ver_common).replace('.','') )
  
  date = str(datetime.now())

  # Addons...
  public_ip_addon = '--external_ip_address=ephemeral' if public_ip == True else '--external_ip_address=none'
  if (public_ip.__class__ == str):
    public_ip_addon = '--external_ip_address=%s' % public_ip
  image_addon = '--image=%s' % image if image else ''
  disk_addon = ('--disk=%s ' % disk) if disk else ''
  for disk2 in disks:
    disk_addon += ('--disk=%s ' % disk2) if disk2 else ''
  
  deb(disk_addon)

  persistent_boot_disk_opts = '--persistent_boot_disk' if persistent_boot_disk else "--nopersistent_boot_disk"
  
  addinstance_opts = """--tags='%s' \
  --zone='%s' \
  --machine_type='%s' \
  --metadata_from_file=startup-script:%s \
  --metadata=startup-metadata:project:%s:e=py^2 \
  --metadata=author:$USER \
  --metadata=created_by_host:$HOSTNAME \
  --metadata=common_ver:$VER_COMMON \
  --metadata=project_ver:$PROJECT_VER \
  --metadata=date_creation:'%s' \
  --metadata=project:%s \
  --network='%s' \
  %s \
  %s \
  %s \
  %s \
  %s \
""" % ( 
    ','.join(all_tags), zone, machine_type,	startup_script, project, 
	date, project, network, disk_addon, public_ip_addon, image_addon, persistent_boot_disk_opts,
  additional_options 
  )
  command = '''gcutil addinstance '%s' --project=%s:%s --description='[%s.py] %s' \
	%s \
	''' % (name, group ,project, project, description, addinstance_opts)
  deb(command)
  os.system(command)

def gcutil_adddisk(project,diskname,group = default_group, zone = default_zone):
  '''adddisk                    Create a new machine disk.
                           Usage: gcutil.py [--global_flags] adddisk <disk_name> [--command_flags]
                           Flags for adddisk:

gcutil.disk_cmds:
  --description: Disk description.
    (default: '')
  --size_gb: The size of the persistent disk in GB.
    (default: '10')
    (a positive integer)
  --zone: The zone for this disk.
 
Ric TODO add also size_gb and description.
  '''
  execute('''gcutil --project=%s:%s adddisk %s --zone='%s' &''' % (group,project, diskname, zone))


#def autodetect_project(file):
#  '''detects the project automatically. ie:#
#
#  /projects/pincopallo/a.sh#
#
#  Project: "pincopallo"
#  '''
#  ret = os.path.basename(file)
#  return ret[:-3]                       # taking for granted it ends with '.py'

def gsutil_push_files_for_project(project):
  '''This functions pushes into my Google Storage all my per-machine init scripts.
  They are then pulled from init script...
  '''
  ptitle("gsutil-pushing hosts scripts for %s" % project)
  # gsutil multithreaded
  cmd = "touch .placeholder ; \
    gsutil cp projects/riclib/scripts/include.bash gs://gce/projects/_common/include.bash ; \
    gsutil cp .placeholder gs://gce/projects/%s/.placeholder ; \
    gsutil -m cp projects/%s.d/host.*.sh gs://gce/projects/%s/" % (project,project,project)
  print(cmd)
  os.system(cmd)

def common_pre(project):
  print "Welcome to project '%s'" % project
  # gsutil push stuff
  gsutil_push_files_for_project(project)
  os.system('''gcutil addfirewall httpy --description="Incoming http on port 80 allowed in python lib" --allowed="tcp:http"''')

def gcutil_cmd(project,subcommand,group = default_group):
  os.system('gcutil --project=%s:%s %s' % (group,project,subcommand) )

def common_post(project,group = default_group):
  yellow("Post installation '%s'" % project)
  # requires boot script version 1.2.13 or more:
  # if there is a www host it pseudo puppetizes it :)
  gcutil_cmd(project, ('push www projects/%s.d/host.*.sh /var/www/boot/'     % project) )
  # the dir rcarlesso has been already created/rightowned with the init script :)
  for host in ('www'):
    gcutil_cmd(project, ('push %s ./var/gcutil-*txt ./var/gcutil-*json /var/www/rcarlesso/' % host) ) # push project stuff there
  
def gcutil_setcommoninstancemetadata(project, arr_keys_values):
  pass

############################################
# String stuff
def yellow(str):
  print "\033[1;33m%s\033[0m" % str
def ptitle(str):
  print "\033[1;37m= %s =\033[0m" % str
