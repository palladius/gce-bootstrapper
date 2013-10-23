#!/bin/bash

VER=1.2

PROJ="google.com:biglamp"
REGION='europe-west1'
ZONE0='europe-west1-a'
ZONE1='europe-west1-b'
PREFIX=${1:-just-test-}


PREFIX="${PREFIX}-"       # Adding a dash always :)
GCUTIL="gcutil --project=$PROJ"
# How to configure GCLB:
# https://cloud.google.com/resources/articles/google-compute-engine-load-balancing-in-action
set -e
set -x

function _gcutil_add() {
    VM="$1"
    ZONE="$2"
    COLOR="$3"

    $GCUTIL addinstance "${PREFIX}$VM" \
      --description "Test WWW machine to demonstrate GCLB, created by $0 v$VER" \
      --zone $ZONE \
      --tags gclb,test,deleteme,webbable \
      --machine_type n1-standard-1 \
      --metadata bgcolor="$COLOR" \
      --metadata provisioning_script="$0 v$VER" \
      --nopersistent_boot_disk \
      --image debian-7 \
      --metadata_from_file=startup-script:gclb.d/direct.provisioner-webserver1.sh &

}

# Configuring Firewall:
$GCUTIL addfirewall ${PREFIX}open-80-and-icmp-to-all --allowed 'tcp:22,tcp:80,icmp' &

_gcutil_add www0 $ZONE0 yellow
_gcutil_add www1 $ZONE0 green
_gcutil_add www2 $ZONE1 red
_gcutil_add www3 $ZONE1 blue

# sleep 2

# Stopping apache on first instance, to check TP Health
$GCUTIL ssh "${PREFIX}www0" "sudo service apache2 stop" &

# Configuring GCLB
$GCUTIL addhttphealthcheck "${PREFIX}basic-check"   # checks on port 80 trivially, no parametric name
$GCUTIL addtargetpool      "${PREFIX}www-tp" --region=$REGION --instances "$ZONE0/${PREFIX}www0,$ZONE0/${PREFIX}www1,$ZONE1/${PREFIX}www2,$ZONE1/${PREFIX}www3" --health_checks="${PREFIX}basic-check"
$GCUTIL addforwardingrule  "${PREFIX}www-fwdrule" --region=$REGION --port_range=80 --target=${PREFIX}www-tp

echo Health:
$GCUTIL gettargetpoolhealth "${PREFIX}www-tp" # | tee .targetpoolhealth.${PREFIX}www-tp.tmp

echo All good.