

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
def pyellow(str):
  print "\033[1;33m%s\033[0m" % str
def ptitle(str):
  print "\033[1;37m= %s =\033[0m" % str