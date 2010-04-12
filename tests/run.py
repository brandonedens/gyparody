#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Gyparody unit test driver
    ~~~~~~~~~~~~~~~~~~~~~~~

    This script runs the Gyparody unit test suite.

    :copyright: Copyright 2007-2009 by the Gyparody team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import sys
from os import path

# always test the gyparody package from this directory
sys.path.insert(0, path.join(path.dirname(__file__), path.pardir))

try:
    import nose
except ImportError:
    print "The nose package is needed to run the Gyparody test suite."
    sys.exit(1)

print "Running Gyparody test suite..."
nose.main()
