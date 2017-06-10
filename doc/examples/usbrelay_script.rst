Example usage of the usbrelay script
####################################

After installation, one should be able to use the usbrelay script 
from the command line::

  usbrelay -h

The settings used to send the serial commands are provided with::

  usbrelay -s

To turn on the first channel of the USB relay, one can use any of 
the following commands::

  usbrelay -c 1,1

or::

  usbrelay -c 1,on

or, to wait 0.2 seconds before turing channel 1 on::

  usbrelay -t 0.2 -c 1,1

Sequences of commands can be strung together.
To turn the first channel on after 0.2 seconds, and off after 5.1 seconds::

  usbrelay -t 0.2 5.1 -c 1,on 1,off

.. note:: The times must be in ascending order.

To apply multiple commands at the same time (limited by the relay hardware) use the "s" character::

  usbrelay -t 0.2 s 5.1 s -c 1,on 2,on 1,off 2,off

Complex sequences of commands can be constructed::

  usbrelay -t 0 s s s 5.1 s s s s s s s 10.2 s s s -c 1,1 3,1 5,1 7,1 1,0 3,0 5,0 7,0 2,1 4,1 6,1 8,1 2,0 4,0 6,0 8,0
