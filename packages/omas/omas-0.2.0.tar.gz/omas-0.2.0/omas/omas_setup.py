from __future__ import print_function, division, unicode_literals

# --------------------------------------------
# external imports
# --------------------------------------------
import os
import sys
import glob
import json
import copy
from collections import OrderedDict
import re
import numpy
from pprint import pprint

# Python3/2 import differences
if sys.version_info < (3, 0):
    import cPickle as pickle
    from collections import MutableMapping
else:
    basestring = str
    unicode = str
    import pickle
    from collections.abc import MutableMapping

# --------------------------------------------
# rcparams
# --------------------------------------------
omas_rcparams = {
    'consistency_check': True,
}

# --------------------------------------------
# configuration of directories and IMAS infos
# --------------------------------------------
imas_json_dir = os.path.abspath(str(os.path.dirname(__file__)) + '/imas_structures/')

separator = '.'

if 'IMAS_VERSION' in os.environ:
    default_imas_version = os.environ['IMAS_VERSION']
else:
    default_imas_version = re.sub('_', '.', os.path.split(sorted(glob.glob(imas_json_dir + os.sep + '*'))[-1])[-1])
