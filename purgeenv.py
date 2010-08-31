#! /usr/bin/env python

import os

keepers = ['_', 'TERM', 'SHELL', 'SSH_TTY', 'USER', 'HOME', 'SSH_CLIENT', 'SSH_CONNECTION',]

for key in os.environ:
    if key not in keepers:
        print 'unset ' + key + ';'

print 'exec ' + os.environ['SHELL'] + ' --login'
