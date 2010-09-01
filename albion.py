#! /usr/bin/env python

import os
import sys

keepers = ['_', 'TERM', 'SHELL', 'SSH_TTY', 'USER', 'HOME', 'SSH_CLIENT', 'SSH_CONNECTION', 'DISPLAY', ]

def usage():
    print >>sys.stderr, 'Usage:'
    print >>sys.stderr, '  albion command'
    print >>sys.stderr, ''
    print >>sys.stderr, 'command is one of:'
    print >>sys.stderr, '  load'
    print >>sys.stderr, '  unload'

def load():
    print >>sys.stderr, "this is load"

def unload():
    print >>sys.stderr, "this is unload"
    purgeenv()

def list_envs():
    """output of this should not be evaled"""
    path_var = 'ALBION_ENV_PATH'
    if path_var not in os.environ:
        print path_var + ' is not set'
        sys.exit(-1)
    for envdir in os.environ[path_var].split(':'):
        for env in os.listdir( envdir ):
            print env

def purgeenv():
    """output of this should be evaled"""
    for key in os.environ:
        if key not in keepers:
            print 'unset ' + key + ';'
    print 'exec ' + os.environ['SHELL'] + ' --login'

commands = { 'list_envs': list_envs,
             'lo': load,
             'loa': load,
             'load': load,
             'un': unload,
             'unl': unload,
             'unlo': unload,
             'unloa': unload,
             'unload': unload, }

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)
    
    if sys.argv[1] in commands:
        commands[sys.argv[1]]()
    else:
        print >>sys.stderr, 'there is no "%s" command' % sys.argv[1]
        sys.exit(-1)

if __name__ == "__main__":
    main()
