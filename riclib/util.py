

############################################
# Debug stuff
def deb(s, debug=False):
  '''Colored Debug function'''
  if len(s) > 0 and debug:
    print "\033[1;30m#DEB# {}\033[0m".format(s) 


def debug_app():
    '''Sets debug.'''
    import ipdb
    ipdb.set_trace()

############################################
# String stuff
def yellow(str):
  return "\033[1;33m{}\033[0m".format(str)
def pyellow(str):
  print yellow(str)
def ptitle(str):
  print "\033[1;37m= %s =\033[0m" % str