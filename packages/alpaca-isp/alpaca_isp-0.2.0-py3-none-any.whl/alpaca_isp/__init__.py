# Copyright 2017 Clayton G. Hobbs
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""In-system programming tool for LPC microcontrollers"""

__author__ = "Clayton G. Hobbs"
__version__ = "0.2.0"

import argparse
import sys

import intelhex

from alpaca_isp.chips import chips
from alpaca_isp.exceptions import *
from alpaca_isp.lpc import *


def create_lpc(tty, baudrate=DEFAULT_BAUDRATE, clock=DEFAULT_CLOCK,
        timeout=DEFAULT_TIMEOUT, control=False, try_sync=None,
        verbose=False):
    """Create an object of the appropriate LPC subclass for the chip"""
    # Open the LPC
    lpc = LPC(tty, baudrate=baudrate, clock=clock, timeout=timeout)
    lpc.open()

    # Enter ISP mode if we've been asked to
    if control:
        lpc.enter_isp()

    # Synchronize with the microcontroller
    if verbose:
        print("Synchronizing", end="", flush=True)
    try:
        lpc.synchronize(max_tries=try_sync, verbose=verbose)
    except RecvTimeout:
        lpc.close()
        if verbose:
            print(" failed")
        raise
    except KeyboardInterrupt:
        lpc.close()
        if verbose:
            print()
        raise
    if verbose:
        print()

    # Turn the LPC object into the right type
    chip = chips[lpc.part_id]
    return chip.family(lpc, chip)



def main():
    """Entry point for Alpaca ISP command line tool"""
    # Make the argument parser
    parser = argparse.ArgumentParser(
            description="Flash an LPC microcontroller")
    parser.add_argument("file", metavar="file", nargs="+", type=str,
            help="Intel HEX file to flash to the microcontroller")
    parser.add_argument("tty", metavar="tty", type=str,
            help="the tty to which the microcontroller is attached")
    parser.add_argument("-b", "--baudrate", type=int,
            default=DEFAULT_BAUDRATE,
            help="baud rate used for communication (default: %(default)s)")
    parser.add_argument("-c", "--clock-khz", type=int, default=DEFAULT_CLOCK,
            help="microcontroller's clock frequency in kHz "
            "(default: %(default)s)")
    parser.add_argument("-t", "--timeout", type=float,
            default=DEFAULT_TIMEOUT,
            help="timeout for reading data from the microcontroller in "
            "seconds (default: %(default)s)")
    parser.add_argument("-e", "--erase", action="store_true",
            help="erase all the microcontroller's flash before flashing")
    parser.add_argument("--no-start", action="store_true",
            help="do not start the microcontroller after flashing")
    parser.add_argument("--try-sync", type=int,
            help="maximum number of tries to synchronize with the "
            "microcontroller")
    parser.add_argument("-n", "--control", action="store_true",
            help="control RS232 lines to enter ISP mode (/RST = DTR, /ISP = "
            "RTS)")
    parser.add_argument("-r", "--verify", action="store_true",
            help="verify that the data were written correctly after flashing")

    # Parse arguments
    args = parser.parse_args()

    # Open the LPC
    try:
        lpc = create_lpc(args.tty, baudrate=args.baudrate,
                clock=args.clock_khz, timeout=args.timeout,
                control=args.control, try_sync=args.try_sync, verbose=True)
    except (RecvTimeout, KeyboardInterrupt):
        sys.exit(1)

    # Unlock the chip
    lpc.unlock()

    # Erase the flash if we've been asked to
    if args.erase:
        print("Erasing all flash sectors")
        lpc.prepare_write()
        lpc.erase()

    # Load the files
    ih = intelhex.IntelHex()
    for f in args.file:
        ih.fromfile(f, format="hex")

    # Write the files to flash
    try:
        lpc.flash_hex(ih, verbose=True)
    except ISPError as e:
        if e.args[0] == ReturnCode.CODE_READ_PROTECTION_ENABLED:
            print("Error: code read protection is enabled")
            print("Unable to flash, exiting")
        sys.exit(2)

    # Verify that the flash has been written correctly if we've been asked to
    if args.verify:
        try:
            lpc.verify(ih, verbose=True)
        except ISPError as e:
            if e.args[0] == ReturnCode.CODE_READ_PROTECTION_ENABLED:
                print("Error: code read protection is enabled")
                print("Unable to verify, continuing")
            else:
                print("Flash verification failed, exiting")
                sys.exit(3)

    # Start the program if we haven't been asked not to
    if not args.no_start:
        print("Starting program")
        lpc.go()

    lpc.close()
