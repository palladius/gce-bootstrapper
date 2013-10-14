#!/bin/bash

###########################################################################################
# Riccardo startup script for his machines. Use at your own risk!
# Startup Script, see here: https://developers.google.com/compute/docs/howtos/startupscript
# This script shouldnt substitute Puppet/Chef! Dont make it too complicated! Ideally you
# should just get it up and running and autoconfigurable from Puppet/Chef/whatever
#
# to call this script, you just call
#
# gcutil addinstance INSTANCENAME
#
# Note this only work with debian/ubuntu based distros.
###########################################################################################

VER=1.4.1

FIRST_BOOT_HISTORY='
20131014 1.4.1  riccardo Copying this script to /root/
20131014 1.4.0  riccardo Starting to integrate with new GitHub repo. Adding dynamic $BUCKET
20120924 1.3.9  riccardo sakura bin is now executable also by normal users 
20120924 1.3.8  riccardo gsutil-downloading /opt/google/lib/include.bash
20120924 1.3.7  riccardo Added /opt/google/bin/ to PATH and /o/g/lib/
20120920 1.3.6  riccardo history added, mini thing (bold project) after painful merge
20120919 1.3.5  riccardo added palladia links for projects :)
20120918 1.3.4  riccardo sakura & my public IP, curling description
20120727 1.3.3  riccardo observability, more control on host-script
20120727 1.3.2  riccardo bugfix, creating /var/log/riccardo
20120727 1.3.1  riccardo downloads and execute per-host script! Puppet Im better than you! :)
20120727 1.2.17 riccardo adding PROJECT to base metadata
20120726 1.2.16 riccardo removing rump (too much time)
20120726 1.2.15 riccardo adding gsutil configuration as Riccardo (potentially dangerous!) and BASH_PREAMBLE
20120627 1.2.14 riccardo better aliases, auto format disks and mount :)
20120627 1.2.13 riccardo /var/www/boot/, cowsay, cleanup, wget from www
20120620 1.2.12 riccardo +iperf ,PS1 in bashrc_aliases, /opt/google/VERSION nmap
20120620 1.2.11 riccardo Added netcat and Dublin tz
20120615 1.2.10 riccardo Added gsutil + per-host script (cant work)
20120615 1.2.9  riccardo sendmail
20120615 1.2.8  riccardo newer gems
20120614 1.2.7  riccardo etckeeper on git, aptget remove, gems, bash_aliases
201206?? 1.2.6  riccardo ??
20120604 1.2.4  riccardo Added puppet rump
20120604 1.2.3  riccardo Added /opt/google and pushed metadata into it
20120604 1.2.2  riccardo Supports per-project behaviour thru metadata
20120604 1.2.1  riccardo Installs nifty packages like git, etckeeper, puppet, facter, ...
'
###########################################
# Configuration stuff
# apt-get install stuff
INSTALLANDA_PACKAGES='apache2 git vim facter puppet etckeeper bzr make rubygems ruby nagios-nrpe-server sendmail netcat netcat6 iperf nmap cowsay links'
REMOVANDA_PACKAGES='nano emacs'
GEMS_INSTALLANDA='ric rubygems-update' # rump 
GEM_POST_OPTS=' --no-ri --no-rdoc'
# rubygems-update : allows rubygems to go over 1.3.5 on old Ubuntu..
ADMIN_EMAIL=palladiusbonton@gmail.com
# TODO peek from METADATA!
ADMIN_USER=rcarlesso
 # TODO take it from metadata
BASH_PREAMBLE='# This file was created by common-startup-script.sh. Edit at your own risk
# At next reboot, it *should* be overwritten again (but nowe its not yet maybe a bug in documentation?)'

METADATA=$(curl http://metadata/0.1/meta-data/attributes/startup-metadata)
PROJECT=$( echo "$METADATA" | cut -f 2 -d: )
BUCKET=$( curl http://metadata/0.1/meta-data/attributes/mybucket )
ADDON=`cat /opt/google/PROJECT`
ADDON2=`cat /opt/google/ADDON`


############################################
# common for all machines in this project

set -x

if [-f /opt/google/lib/include.bash ]; then
  . /opt/google/lib/include.bash
fi

cp "$0" "/root/startup-script-copy-$(date +%s).sh"

apt-get update
apt-get install -y $INSTALLANDA_PACKAGES
apt-get purge   -y $REMOVANDA_PACKAGES

# before etckeeper
git config --global user.name "Riccardo auto-gcompute-robot"
git config --global user.email rcarlesso+gcomputerobot@google.com


# etckeeper installation
sed -i 's:#\(VCS="git"\):\1:'  /etc/etckeeper/etckeeper.conf 
sed -i 's:^\(VCS="bzr"\):#\1:' /etc/etckeeper/etckeeper.conf

etckeeper init
etckeeper commit -m 'first commit by init script with bazaar or maybe git by Riccardo'

gem install $GEMS_INSTALLANDA $GEM_POST_OPTS &    # takes time and i dont care to wait for it!

##############################################
# Bash aliases file on Ubuntu!
cat <<ALIASES_EOF > ~/.bash_aliases
  ######################################################################
  # This file is written by the init script. Should never change, so...
  # edit at will! Riccardo
  #
  # Project:           $PROJECT
  # Hostname:          $(hostname)
  # Date:              $(date)
  # StartupScript ver: $VER
  ######################################################################
  
  alias gcutil_init_version='$VER'
  alias gcutil_machine_created='$(date)' # should be fixed
  alias gcutil_project='echo $PROJECT'
  alias sb='source ~/.bashrc'
  alias cdg='cd /opt/google/'
  alias sauu='sudo apt-get update && sudo apt-get dist-upgrade'
  alias aiuto='getmetadata description 2>/dev/null| cowsay'

  export PS1='\u@$(hostname -f):\w\$ '
  
  # for metadata and other stuff
  if [ -f /opt/google/lib/include.bash ]; then
    . /opt/google/lib/include.bash
  fi
  
  # for binaries in rubygems
  export PATH=\$PATH:/var/lib/gems/1.8/bin/:/opt/google/sbin:/opt/google/bin:/usr/games/:/root/git/sakura/bin/
  
  # maybe we could mute it
  echo 'Beware, with great powers comes great responsibility. Try also "gce-public-ip". Riccardo' | /usr/games/cowsay 

ALIASES_EOF

# copying the same for rcarlesso user
cp ~/.bash_aliases ~rcarlesso/.bash_aliases
chown    rcarlesso ~rcarlesso/.bash_aliases

if [ -f /home/$ADMIN_USER/ ] ; then
  cp ~/.bash_aliases ~$ADMIN_USER/.bash_aliases
  chown $ADMIN_USER ~$ADMIN_USER/.bash_aliases
fi

#index which contains the Project name :)
cat <<WWW_EOF > /var/www/index.html
<html><body>
  <h1>Host $HOSTNAME ($PROJECT)</h1>
  <p>This page was created automatically from Riccardo mephistophelic script <tt><b>common-startup-script.sh v$VER</b></tt> (from $0) for project <b>$PROJECT</b>!</p>
  <p>See more docs <a href='https://developers.google.com/compute/docs/howtos/startupscript'>HERE</a>. Thanks, Riccardo</p>

  <h3><a href='http://173.255.116.17/rcarlesso/'>Palladia links</a></h3>
  
  * 
   <a href='http://173.255.116.17/rcarlesso/gcutil-listinstances-$PROJECT.txt'>Instances</a> 
   <a href='http://173.255.116.17/rcarlesso/gcutil-listfirewalls-$PROJECT.txt'>Firewalls</a> 
   <a href='http://173.255.116.17/rcarlesso/gcutil-getproject-$PROJECT.txt'>Project</a>
   <a href='http://173.255.116.17/rcarlesso/gcutil-getproject-$PROJECT.json'>P.json</a>
   <a href='http://173.255.116.17/rcarlesso/gcutil-listzones-$PROJECT.txt'>Zones</a> 
  <br/>

  <h3>Custom metadata</h3>

  
  <p>Host-peculiar metadata: <b>$METADATA</b>
  <p>hostname: <b>$HOSTNAME</b>
  <p>Project description: <pre>"$(curl http://metadata/0.1/meta-data/attributes/description )"</pre>

</body></html>
WWW_EOF

############################################################################
# Sets 'gsutil' authentication!
#
# Note: potentially vulnerable!!! do sth better TODO @security
############################################################################
cat << BOTO_EOF > /root/.boto
# $BASH_PREAMBLE
[Credentials]
gs_oauth2_refresh_token = 1/tUJTUltZ4mnaL1F6hMrMw74Vg-TARHmsndGENeGdEMc
[Boto]
https_validate_certificates = True
[GSUtil]
default_api_version = 2
default_project_id = 613126411804
[OAuth2]
BOTO_EOF

cp /root/.boto  ~rcarlesso/.boto
chown rcarlesso ~rcarlesso/.boto

# timezone... needs a dpkg-reconfgiure tzdata or reboot i guess :P
echo Europe/Dublin > /etc/timezone

mkdir -p /opt/google/bin /opt/google/sbin /opt/google/lib /opt/google/etc /opt/google/tmp /var/log/riccardo/  /var/www/rcarlesso
chown rcarlesso /var/www/rcarlesso/

ln -s /opt/google /root/google

# tells the machine what we've done so far
cat <<EOF >> /opt/google/HISTORY
= Project '$PROJECT' =
$(date) [riccardo] Added simple startup script: $0
EOF

#############################################
#Setting up /var/www/boot to scp files there
mkdir -p /var/www/boot/ 
chown -R $ADMIN_USER

# OMG
curl http://metadata/0.1/meta-data/description                 > /opt/google/MACHINE_DESCRIPTION
curl http://metadata/0.1/meta-data/tags                        > /opt/google/MACHINE_TAGS
curl http://metadata/0.1/meta-data/attributes/author           > /opt/google/USER
curl http://metadata/0.1/meta-data/attributes/startup-metadata > /opt/google/STARTUP_METADATA
echo $VER                                                      > /opt/google/STARTUP_SCRIPT_VERSION
curl http://metadata/0.1/meta-data/attributes/project          > /opt/google/PROJECT
for metadataz in $( curl http://metadata/0.1/meta-data/attributes/ ) ; do 
  curl http://metadata/0.1/meta-data/attributes/$metadataz >> METADATA-$metadataz.txt 
done

# my puppet script to see what the craic is
#curl https://raw.github.com/palladius/puppet-rump/master/first-install.sh > /tmp/rc_exec_once.sh && bash /tmp/rc_exec_once.sh &

# cloning sakura
cd /root/ && 
 mkdir git && 
  cd git &&  
   git clone git://github.com/palladius/sakura &&
     cat /root/git/sakura/templates/bashrc.inject >> /root/.bashrc

      touch /root/errors-retrieving-hostbased-init-script-w-gsutil.touch

############################################
# Format disks, if any:
cat <<FORMATDISKS_EOF > /opt/google/sbin/format-disks-by-riccardo
#!/bin/sh

# this script was made by Riccardo Carlesso <rcarlesso@google.com> as part
# of his init scripts. Use at your own risk. If misused, you can completely
# delete an existing disk/partition.

cd /dev/disk/by-id/
for diskdev in virtio-disk-1 virtio-disk-2 virtio-disk-3 virtio-disk-4 virtio-disk-5 ; do
  if [ -h \$diskdev ] ; then # exists and symlink
    echo DEB Trying to make it work with: /mnt/gdisk-\$diskdev 
    mkdir -p /mnt/gdisk-\$diskdev
    mount -t ext4 \$diskdev /mnt/gdisk-\$diskdev && 
      echo mounted \$diskdev &&
        touch /mnt/gdisk-\$diskdev/mounted-without-formatting.touch || 
    mkfs.ext4 /mnt/gdisk-\$diskdev &&
      echo formatted \$diskdev && 
        mount -t ext4 \$diskdev /mnt/gdisk-\$diskdev &&
          echo also mounted \$diskdev &&
            touch /mnt/gdisk-\$diskdev/formatted-and-mounted.touch
  else
    echo Apparently no file named: /dev/disk/by-id/\$diskdev
  fi
done  
FORMATDISKS_EOF

chmod 755 /opt/google/sbin/format-disks-by-riccardo /root/ /root/git /root/git/sakura /root/git/sakura/bin

echo $VER > /opt/google/VERSION

echo "$FIRST_BOOT_HISTORY" >> opt/google/FIRST_BOOT_HISTORY

touch /root/03-end-of-common-startup-script-now-calling-custom.touch

###################################################################################################
# Uses gsutil to download a file for itself. This is sooooo Puppety! :)
# It cant work because there's no way (yet) to inject the key in the hosts
################################################################################################### 
GSTORAGE_HOST_SPECIFIC_SCRIPT_URL="$BUCKET/addons/$ADDON/host.$HOSTNAME.sh"
LOCAL_PATH=/root/my-personal-init-script.sh
gsutil cp $BUCKET/projects/_common/include.bash /opt/google/lib/include.bash &&
 gsutil cp "$GSTORAGE_HOST_SPECIFIC_SCRIPT_URL" $LOCAL_PATH && 
  /bin/bash $LOCAL_PATH 1>/var/log/riccardo/host-script.out 2>/var/log/riccardo/host-script.err &&
    mv  $LOCAL_PATH "$LOCAL_PATH.executed-with-exit-$?" ||
      touch /root/errors-retrieving-hostbased-init-script-w-gsutil.touch

touch /root/04-succesfully-launched-custom-script-$PROJECT-$HOSTNAME.touch

echo Subject: I was installed | sendmail $ADMIN_EMAIL

touch /root/05-end-of-common-startup-script-YOU_SHOULD_BE_GRAND.touch
#wget http://www/boot/host.$(hostname).sh > /root/bootme-from-www-riccardo.sh
