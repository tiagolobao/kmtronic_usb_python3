# Setup file to distribute usbrelay package using distutils.
#
# The python-usbrelay package allows one to control a USB relay bank. 
license_text = "(C) 2012 David Schryer GNU GPLv3 or later."
__copyright__ = license_text

import os
import glob
from distutils.core import setup

pn = 'usbrelay'
pn_scripts = glob.glob('scripts/{0}*'.format(pn))

setup(name=pn,
      version='0.1',
      license=license,
      package_dir={pn:pn},
      packages=[pn],
      scripts=pn_scripts,
      long_description=open('README.txt').read(),
      )
