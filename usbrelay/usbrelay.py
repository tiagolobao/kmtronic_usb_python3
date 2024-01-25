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

import serial
            
class Relay(object):
    """This is an object used to talk with a USB relay bank.

    It provides a function to send commands and a function
    to output the serial connection settings.
    """

    def __init__(self, relay_type, serialPort):
        if relay_type == 'KMTronic_8':
            ch = range(1,9)
        else:
            msg = 'This relay_type is not available.'
            raise NotImplementedError(msg, relay_type)

        self.serialPort = serialPort
        self.channels = ch
        self.relay_type = relay_type
        self.states = [0, 1, 'on', 'off']
        self.serialInstace = serial.Serial(
            port=self.serialPort,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            xonxoff=True,
        )

    def output_parameters(self):
        """Outputs the parameters used to control the USB relay bank.
        """
        print( '{0} : {1}'.format(self.serialInstace.port, self.serialInstace.getSettingsDict()) )

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
            
        packet = bytearray(3)
        packet[0] = 0xFF
        packet[1] = channel
        packet[2] = state

        if verbose:
            msg = 'Switching channel {0} of a {1} {2} by sending {3}'
            print(msg.format(channel, rt, stp, packet))

        if not self.serialInstace.isOpen():
            self.serialInstace.open()
        self.serialInstace.write(packet)
