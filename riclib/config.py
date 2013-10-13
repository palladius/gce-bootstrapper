"""config.py

This file makes sure the config file is parsed correctly.

It must have:

"""

import re
import yaml
from util import deb

default_ymlfile = '../config.yml' # here we are one dir below :)
mandatory_fields = ['project_id', 'bucket', 'metadata', 'admin', 'defaults', 'dryrun']
mandatory_secondary_fields = {
  'admin':    ['email', 'name'],
  'defaults': ['zone', 'machine_type', 'network' ],
}

def getConfigYaml(ymlfile=default_ymlfile):
  """Returns a dict with configuration.

  Also provides correct messaging in case of error/
  """
  deb("Conf file: {}".format(ymlfile))
  conf = {}
  try:
    yml = open(ymlfile, 'r')
    whole_conf = yaml.load(yml)
    deb( whole_conf)
    conf = whole_conf['production']
    deb( conf)
  except (OSError, IOError) as e:
    print """YAML not found. Maybe you forgot to do this:
    1. cp {f}.dist {f}
    2. vi {f}                 # edit as needed
    """.format(f=ymlfile)
    exit(2)
  except Exception as e:
    print "Generic exception: {}".format(e)
    exit(3)
  explaination = CheckValidity(conf)
  if explaination != '':
    print "Configuration is invalid: {}".format(explaination)
    exit(4)
  return conf


def CheckValidity(config):
    """Asserts conig has some values.

    ie: 
    - project_id (string or number), 
    - bucket (string starting with gs://)
    - metadata (dict)
    - admin must have email and name
    - defaults must have zone, machine_type and network
    """
    

    for i in mandatory_fields:
      if i not in config.keys():
        return "'{}' mandatory key1 missing".format(i)

    for f1 in mandatory_secondary_fields.keys():
        print "f1: {f1}"
        subkeys = mandatory_secondary_fields[f1]
        for f2 in subkeys:
            if not f2 in config[f1].keys():
                return "'{}.{}' mandatory key2 missing".format(f1, f2)

    if not re.search('^gs://.*',config['bucket']):
       return "'bucket' conf field ('{}') must start with 'gs://'".format(config['bucket'])

    return ''