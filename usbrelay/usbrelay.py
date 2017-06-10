""" Provides Relay class for general use.

Module content
--------------
"""
# Author: David Schryer
# Created: 2012
# The python-usbrelay package allows one to control a USB relay bank.
license_text = "(C) 2012 David Schryer GNU GPLv3 or later."
__copyright__ = license_text

__autodoc__ = ['Relay']
__all__ = __autodoc__

import os
import time
import serial
import serial.tools.list_ports
import subprocess

from struct import pack, unpack, calcsize
            
class Relay(object):
    """This is an object used to talk with a USB relay bank.

    It provides a function to send commands and a function
    to output the serial connection settings.
    """

    def __init__(self, relay_type):
        if relay_type == 'KMTronic_8':
            ch = range(1,9)
        else:
            msg = 'This relay_type is not available.'
            raise NotImplementedError(msg, relay_type)

        self.tty_port = list(serial.tools.list_ports.grep("04d8:f55e"))[0][0]
        self.channels = ch
        self.relay_type = relay_type
        self.states = [0, 1, 'on', 'off']
        

    def _make_serial_object(self, tty_port):
        '''
        Makes a serial object that can be used for talking with a usbrelay.
        '''
        return serial.Serial(port=tty_port,
                             baudrate=9600,
                             parity=serial.PARITY_NONE,
                             stopbits=serial.STOPBITS_ONE,
                             bytesize=serial.EIGHTBITS,
                             xonxoff=True,
        )

    def output_parameters(self):
        """Outputs the parameters used to control the USB relay bank.
        """
        so = self._make_serial_object(self.tty_port)
        print(so.getPort() + ' : ' + `so.getSettingsDict()`)

    def set(self, channel=None, state=None, verbose=False):
        """Sets the state of a given channel.

        Parameters
        ----------
        channel : int
          Channel to set state of.
        state : bool or str
          Set state of channel to on or off. Must be in [0, 1, 'on', 'off'].
        verbose: bool
          Flag to specify verbocity.

        Raises
        ------
        UserWarning
          -- If the state is not in [0, 1, 'on', 'off'].
          -- If the channel is not available to this USB relay.
        """

        channels = self.channels
        states = self.states
        rt = self.relay_type
        if channel not in channels:
            msg = 'The {0} only has the following channels: {1}'.format(rt, channels)
            raise UserWarning(msg, channel)
        if state not in states:
            msg = 'The state must be one of {0}'.format(states)
            raise UserWarning(msg, state)
        if state == 'on' or state == 1:
            state = 1
            stp = 'on'
        if state == 'off' or state == 0:
            state = 0
            stp = 'off'
            
        int_msg = [255, channel, state]
        byte_msg = map(chr, int_msg)
        packet = pack('=ccc', *byte_msg)

        if verbose:
            msg = 'Switching channel {0} of a {1} {2:3} by sending int:{3} = byte:{4}'
            print(msg.format(channel, rt, stp, int_msg, byte_msg))

        so = self._make_serial_object(self.tty_port)
        if not so.isOpen():
		so.open()
        so.write(packet)

if __name__ == '__main__':

    r = Relay('KMTronic_8')

    cmds = []
    for ch in r.channels:
        cmds.append((ch, 1))
        cmds.append((ch, 0))
    while True:
    	for cmd in cmds:
        	r.set(*cmd, verbose=True)
        	time.sleep(2)
