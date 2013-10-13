


def deb(str, debug=True):
  '''Colored Debug function'''
  if len(str) > 0 and debug:
    print "\033[1;30m#DEB# %s\033[0m\n" % str 


def debug_app():
    '''Sets debug.'''
    import ipdb
    ipdb.set_trace()
