


def deb(s, debug=True):
  '''Colored Debug function'''
  if len(s) > 0 and debug:
    print "\033[1;30m#DEB# {}\033[0m".format(s) 


def debug_app():
    '''Sets debug.'''
    import ipdb
    ipdb.set_trace()
