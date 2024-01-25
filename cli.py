#!/usr/bin/python
# -*- mode: python -*-
"""
Script to switch relay states.
"""
# The python-usbrelay package allows one to control a USB relay bank.
license_text = "(C) 2012 David Schryer GNU GPLv3 or later."
__copyright__ = license_text

import time
import textwrap
import argparse

from usbrelay.usbrelay import Relay

def time_command(command):
    if command != 's':
        try:
            A = float(command)
        except ValueError:
            msg = 'A time must be either a float or "s" to indicate at the same time as the last command'
            raise argparse.ArgumentTypeError(msg, command)
    else:
        A = command
    return A
    
def command(command):

    out = command.split(',')

    if len(out) != 2:
        msg = "Commands must be A,B where A is the channel, and B is the state."
        raise argparse.ArgumentTypeError(msg, command)

    try:
        A = int(out[0])
    except ValueError:
        msg = "Commands must be A,B where A is an integer, and B is the state."
        raise argparse.ArgumentTypeError(msg, command)

    B = out[1]
    if len(B) == 1:
        try:
            B = int(B)
        except ValueError:
            msg = "Commands must be A,B where A is an integer, and B is the state.  B not in [0, 1, 'on', 'off']"
            raise argparse.ArgumentTypeError(msg, command)
    else:
        B = B.strip()
    
    if B not in [0,1, 'on', 'off']:
        msg = "State portion of command must be in [0,1,'on','off'], given: {0}".format(B)
        raise argparse.ArgumentTypeError(msg, command)
        
    return A, B

        
def make_argument_parser():
    '''Returns argument parser for this script.
    '''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''
                                     This script allows one to switch the state of a usbrelay 
                                     ========================================================
                                     It currenly only supports the KMTronic usb eight channel
                                     relay controller. Others can easily be added.
                                     Parameters are either I (int), F (float), or S (string).
                                                             
                                     '''),
                                     fromfile_prefix_chars='@')

    fg = parser.add_argument_group('Flag parameters')
    spg = parser.add_argument_group('Setup parameters')
    cpg = parser.add_argument_group('Control parameters')
    
    d = '[default:%(default)s]'
    c = '[choices:%(choices)s]'
    FL = 'F/S'
    ST = 'S'
    CMD = 'I,I/S '

    fg.add_argument("-v", "--verbose", action='store_true',
                    dest="verbose", default=False, 
                    help='Flag to specify if the script should be verbose. {0}'.format(d))

    fg.add_argument("-s", "--output-settings", action='store_true',
                    dest="output_settings", default=False, 
                    help='Flag to specify if the script should output the USB relay settings and exit. {0}'.format(d))
    
    spg.add_argument("-r", "--relay-type", 
                     dest="relay_type", default='KMTronic_8', metavar=ST, choices=['KMTronic_8'],
                     help='Sets the relay type to be used. {0} {1}'.format(d, c))

    spg.add_argument("-p", "--port", 
                     dest="port", default='None', metavar=ST,
                     help='Sets the serial Port to be used [mandatory]. {0}'.format(d))

    cpg.add_argument("-t", "--time-sequence", nargs='+', type=time_command,
                     dest="time_sequence", default=None, metavar=FL, 
                     help='Sequence of times to apply commands.  Must be in ascending order. The "s" character can be used to apply the same time to the next command.')

    cpg.add_argument("-c", "--command-sequence", nargs='+', type=command,
                     dest="command_sequence", default=None, metavar=CMD, 
                     help="Sequence of commands to apply, possibly with a time_sequence. If no sequence is specified, the default is to wait 1 second before applying the second and following commands.")

    return parser

    
def process_arguments(args):

    if args.port == 'None':
        raise Exception("No serial port selected")
    else:
        r = Relay(args.relay_type, args.port)
        r.output_parameters()

    if not args.command_sequence:
        msg = 'A command sequence must be specified (C1,S1 C2,S2 C3,S3).'
        raise UserWarning(msg, args)
        
    if args.time_sequence:
        if len(args.time_sequence) != len(args.command_sequence):
            msg = 'len(command_sequence) != len(time_sequence)'
            raise UserWarning(msg, (args))
    else:
        args.time_sequence = range(len(args.command_sequence))
        assert len(args.time_sequence) == len(args.command_sequence)

    previous = 0
    for t in args.time_sequence:
        if t == 's':
            continue
        if t < 0:
            msg = 'All times must be positive.'
            raise UserWarning(msg, (args))
        if t < previous:
            msg = 'The time sequence must be in ascending order.'
            raise UserWarning(msg, (args))
        else:
            previous = t
            
    for i, t in enumerate(args.time_sequence):
        cmd = args.command_sequence[i]
        if args.verbose:
            print('Waiting {0} seconds to execute command: {1}'.format(t, cmd))
        try:
            time.sleep(t)
        except TypeError:
            pass
            
        r = Relay(args.relay_type, args.port)
        r.set(*cmd, verbose=args.verbose)
        
if __name__ == '__main__':

    p = make_argument_parser()
    args = p.parse_args()
    process_arguments(args)
