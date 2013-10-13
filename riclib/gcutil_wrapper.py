
##################################################
# gcompute library
##################################################

from datetime   import datetime, date, time 
from util       import deb, yellow, ptitle
from subprocess import call

import subprocess
import os

# Zone REading from                                        2012-11-01 manually edited :)
# TODO import from YAML!

# TODO take from conf
#default_tags           = [ 'ricpy', 'torino' ]
#default_zone           = 'europe-west1-b'     # Europe, yay!
#default_machine_type   = 'n1-standard-1'  # for old project its 'standard-1-cpu'
#default_network        = 'default'
#default_startup_script = './projects/riclib/scripts/common-startup-script.sh'


lib_ver_common         = '1.1.0'

lib_ver_history = '''
20131013 1.1.0 pushing common.bash to /projects/common/include.bash
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


def execute(p, cmd):
  """Wrapper to execute code.
  """
  deb("Executing code (dryrun={}): '''{}'''".format(p.dryrun(), cmd))
  if p.dryrun():
    print "#DRYRUN# Wont execute this: '''{}'''".format(cmd)
  else:
      deb("WARNING, executing: {}".format(cmd))
      ret = os.system(cmd)
      print "[CMD] return={}".format(ret)

def gcutil_delinstance(project, name):  
  execute(project, """gcutil --project={} deleteinstance -f '{}'""".format(name, project) )

def gcutil_delinstances(project, names):
  # for name in names:
  #   print("Deleting instance: %s" % name)
  #   gcutil_delinstance(project, name)
  gcutil_delinstance(project, ' '.join(name))


def gcutil_addfirewall(p, name, description, additional_options):
  '''Adds a firewall rule, additional oprtions is just a string... 
  
  sorry for my lazyness  
  ''' 
  command = '''gcutil addfirewall '%s' --project=%s --description='%s' \
  %s ''' % (name, p.id, description, additional_options)
  execute(p, command)

def gcutil_addinstance(project, name, description, 
  public_ip = False,
  tags = [],
  zone = None, 
  machine_type = None,            
  network = None,
  startup_script = None,
  disk = None,
  disks = [] ,
  image = None,
  persistent_boot_disk = False,
  additional_options = ''
  ):
  '''Adds an instance of gcutil (for the moment using the bash script, in the future using
  directly the API written - putacaso - in python!

  Please forgive me, this code is getting more and more unmantainable.
  '''
  print "= Project (should be an object): {} =".format(project)
  if (tags.__class__ != list):
    print "Sorry, I need a list for 'tags', not a %s" % (tags.__class__)
    exit(1)
  if (disks.__class__ != list):
    print "Sorry, I need a list for 'disks', not a %s" % (tags.__class__)
    exit(1)
  if not machine_type:
    machine_type = project.default('machine_type')
  if not zone:
    zone = project.default('zone')
  if not network:
    network = project.default('network')
  if not startup_script:
    startup_script = project.default('startup_script')

  # Using sets to guarantee unicity, then moving back to array
  all_tags = set(tags)
  all_tags.update(project.default('tags'))
  all_tags.update(["gwv%s" % str(lib_ver_common).replace('.','') ])
  all_tags = list(all_tags) # transofmring back to array

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
  
#   addinstance_opts_old = """--tags='%s' \
#   --zone='%s' \
#   --machine_type='%s' \
#   --metadata_from_file=startup-script:%s \
#   --metadata=startup-metadata:project:%s:e=py^2 \
#   --metadata=date_creation:'%s' \
#   --metadata=project_id:%s \
#   --network='%s' \
#   %s \
#   %s \
#   %s \
#   %s \
#   %s \
# """ % ( 
#     ','.join(all_tags), zone, machine_type,	startup_script, project, 
# 	date, project, network, disk_addon, public_ip_addon, image_addon, persistent_boot_disk_opts,
#   additional_options 
#   )
  addinstance_opts = """--tags='{tags}' \
  --zone='{zone}' \
  --machine_type='{mt}' \
  --metadata_from_file=startup-script:{startup} \
  --metadata=startup-metadata:project:{project_id}:maybeIssuesWithNumbers \
  --metadata=date_creation:'{date}' \
  --metadata=project_id:{project_id} \
  --network='{net}' \
  {disk_addon} \
  {public_ip_addon} \
  {image_addon} \
  {persistent_boot_disk_opts} \
  {additional_options} \
""".format(
    tags=','.join(all_tags), 
    zone=zone, 
    mt=machine_type, 
    startup=startup_script, 
    project_id=project, 
    date=date, 
    net=network, 
    disk_addon=disk_addon, 
    public_ip_addon=public_ip_addon,
    image_addon=image_addon,
    persistent_boot_disk_opts=persistent_boot_disk_opts,
    additional_options=additional_options, 
  )


  command = '''gcutil addinstance '%s' --project=%s --description='[%s] %s' \
	%s \
	''' % (name, project.project_id, project.name, description, addinstance_opts)
  execute(project, command)

def gcutil_adddisk(project,diskname, zone = None):
  '''adddisk

Create a new machine disk.
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
  if not zone:
    zone = project.default('zone')
  execute('''gcutil --project=%s adddisk %s --zone='%s' &''' % (project, diskname, zone))



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
  execute(cmd)



def common_pre(project):
  print "Welcome to project '%s'" % project
  # gsutil push stuff
  gsutil_push_files_for_project(project)
  execute('''gcutil addfirewall httpy --description="Incoming http on port 80 allowed in python lib" --allowed="tcp:http"''')

def gcutil_cmd(project,subcommand):
  execute('gcutil --project=%s %s' % (project,subcommand) )

def common_post(project):
  yellow("Post installation '%s'" % project)
  # requires boot script version 1.2.13 or more:
  # if there is a www host it pseudo puppetizes it :)
  gcutil_cmd(project, ('push www projects/{}.d/host.*.sh /var/www/boot/'.format(project)) )
  # the dir rcarlesso has been already created/rightowned with the init script :)
  for host in ('www'):
    gcutil_cmd(project, ('push {} ./var/gcutil-*txt ./var/gcutil-*json /var/www/rcarlesso/'.format(host)) ) # push project stuff there
  
def gcutil_setcommoninstancemetadata(project, arr_keys_values):
  pass


