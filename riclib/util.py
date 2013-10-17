
DEFAULT_DEBUG = True

############################################
# Debug stuff
def deb(s, debug=DEFAULT_DEBUG):
  '''Colored Debug function'''
  DebugSingleton().deb(s)
  #if len(s) > 0 and debug:
  #  print gray("#DEB# {}".format(s))

def debug_app():
    '''Sets debug.'''
    import ipdb
    ipdb.set_trace()

############################################
# String stuff
def yellow(str):
  return "\033[1;33m{}\033[0m".format(str)
def red(str):
  return "\033[1;31m{}\033[0m".format(str)
def green(str):
  return "\033[1;32m{}\033[0m".format(str)
def gray(str):
  return "\033[1;30m{}\033[0m".format(str)

def pyellow(str):
  print yellow(str)
def ptitle(str):
  print "\033[1;37m= %s =\033[0m" % str



class DebugSingleton(object):
    _DEFAULT_DEBUG_VALUE = True
    _instance = None
    _debug = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DebugSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance._debug = cls._DEFAULT_DEBUG_VALUE
            # print "DebugSingleton created only once"
        return cls._instance

    # classmethod
    def setDebug(cls, bool):
        cls._debug=bool

    def deb(self, s):
        if len(s) > 0 and self._debug:
          print "#DEB# {}".format(s)

# call initializer
DebugSingleton()