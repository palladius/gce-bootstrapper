#!/bin/bash

VER=1.0

PROJ="google.com:biglamp"
REGION='europe-west1'
ZONE0='europe-west1-a'
ZONE1='europe-west1-b'
PREFIX='test-gclb2-'

GCUTIL="gcutil --project=$PROJ"
# How to configure GCLB:
# https://cloud.google.com/resources/articles/google-compute-engine-load-balancing-in-action
set -e
set -x

gcutil_add() {
    vm="$1"
    zone="$2"
    $GCUTIL addinstance ${PREFIX}$vm --description "Test WWW machine to demonstrate GCLB, created by $0 v$VER" \
      --zone $zone --tags gclb,test,deleteme \
      --machine_type n1-standard-1 \
      --nopersistent_boot_disk \
      --image debian-7 \
      --metadata_from_file=startup-script:gclb.d/direct.provisioner-webserver1.sh

}

gcutil_add www0 $ZONE0
gcutil_add www1 $ZONE0
gcutil_add www2 $ZONE1
gcutil_add www3 $ZONE1

sleep 2

$GCUTIL ssh ${PREFIX}www0 "sudo service apache2 stop" &

$GCUTIL addhttphealthcheck basic-check   #checks on port 80 trivially, no parametric name
$GCUTIL addtargetpool      ${PREFIX}www-tp --region=$REGION --instances=$ZONE0/${PREFIX}www0,$ZONE0/${PREFIX}www1,$ZONE1/${PREFIX}www2,$ZONE1/${PREFIX}www3 --health_checks="basic-check"
$GCUTIL addforwardingrule  ${PREFIX}www-fwdrule --region=$REGION --port_range=80 --target=${PREFIX}www-tp

yellow "you might weant to try: $GCUTIL gettargetpoolhealth www-tp"