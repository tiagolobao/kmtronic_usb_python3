.. The python-usbrelay package allows one to control a USB relay bank.
   Copyright (C) 2012 David Schryer GNU GPLv3 or later. 


.. sidebar:: python-usbrelay

   :Release: |release|
   :Date: |today|
   :Authors: **David Schryer**
   :Target: developers and administrators
   :status: alpha


Documentation of python-usbrelay
================================

This package allows one to control a USB relay bank. This code 
currently is only tested with a KMTronic USB eight bank relay, 
however, can be extended to work with any device.  

This package was created with and includes only free software and is
licensed under GPLv3 or any later version.  A copy of this license 
is found in the file gpl-3.0.txt.  

The python-usbrelay library uses the excellent python-serial library.

Contents:    
---------

.. toctree::
   :maxdepth: 2

   api/usbrelay

Installation:
-------------
Install with one of these commands::

  python setup.py install --prefix=/usr/local

or::

  python setup.py install

Script:
--------
The usbrelay script that is installed with this package is self documenting.

.. toctree::
   :maxdepth: 2

   examples/usbrelay_script

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`


