#! /usr/bin/env python

import os

for key in os.environ:
    print 'unset ' + key
