#! /usr/bin/env python

import os
import sys

keepers = ['_', 'TERM', 'SHELL', 'SSH_TTY', 'USER', 'HOME', 'SSH_CLIENT', 'SSH_CONNECTION',]

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

def purgeenv():
    for key in os.environ:
        if key not in keepers:
            print 'unset ' + key + ';'
    print 'exec ' + os.environ['SHELL'] + ' --login'

commands = { 'lo': load,
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
