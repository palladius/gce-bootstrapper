###############################################################################
# This file should be put into the cloud with gsutil, then installed by the 
# common script. Then include by instances who want that (ideally I should find
# a mechanism to autoinclude it, like copying a common header into the scripts
# and downloading the second part after it).
#
# Destination should be:
#
#   gs://BUCKET/projects/_common/include.bash
#
###############################################################################

INCLUDE_VERSION=0.9.2

# this gets a metadata
# TODO if metadata doesnt exist, $stderr.puts and return empty string 
# or '_NOT_FOUND_'
# BUG: if called in a pipe, it will publish some unwanted more strings!
function getmetadata() {
  # TODO check for 404 inside the answer, if so return error.
  # sth like this:
  # curl http://metadata/0.1/meta-data/attributes/ | egrep ^$1\$
   curl http://metadata/0.1/meta-data/attributes/$1
}

