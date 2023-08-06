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
"""Interfaces for in-system programming of LPC microcontrollers"""

import struct
import time
from enum import Enum

import serial

from alpaca_isp.exceptions import *


DEFAULT_BAUDRATE = 115200
DEFAULT_CLOCK = 12000
DEFAULT_TIMEOUT = 0.1


class LPC:
    """Interface for LPC in-system programming"""

    def __init__(self, tty, baudrate=DEFAULT_BAUDRATE,
            clock=DEFAULT_CLOCK, timeout=DEFAULT_TIMEOUT):
        # If the first parameter is an LPC, initialize self from that
        if isinstance(tty, LPC):
            o = tty
            self._tty = o._tty
            self._baudrate = o._baudrate
            self._clock = o._clock
            self._timeout = o._timeout
            self._echo = o._echo
            try:
                self._uart = o._uart
            except AttributeError:
                # If there's no o._uart, that's not a problem
                pass
        # Otherwise, initialize from the parameters
        else:
            self._tty = tty
            self._baudrate = baudrate
            self._clock = clock
            self._timeout = timeout
            self._echo = True

    def open(self):
        """Open the serial port to communicate with the microcontroller"""
        self._uart = serial.Serial(self._tty, baudrate=self._baudrate,
                timeout=self._timeout)

    def _readline(self):
        """Read a line terminated with b'\r\n'"""
        s = b""
        while True:
            c = self._uart.read(1)
            if not c:
                # If we timed out, give up
                raise RecvTimeout(s)
            s += c
            if s.endswith(b"\r\n"):
                return s

    def _writeline(self, line, plain=False):
        """Write a line to the microcontroller and read the echoed response

        If plain is True, the command is taken to be raw binary data.
        """
        self._uart.write(line)
        self._uart.flush()

        # If echo is disabled, don't try to read back what we sent
        if not self.echo:
            return

        # Read the response, raising the exception if there is one
        if plain:
            response = self._uart.read(len(line))
        else:
            response = self._readline()
        # If we got the wrong response, raise an exception
        if response != line:
            raise ISPError("Wrong text echoed: {}".format(response))

    def _send_command_raw(self, cmd):
        """Send a command to the microcontroller, returning bytes"""
        self._writeline(cmd)
        return self._readline()

    def _send_command(self, cmd):
        """Send a command to the microcontroller, returning the result"""
        r = self._send_command_raw(cmd)
        r = ReturnCode(int(r))
        if r != ReturnCode.CMD_SUCCESS:
            raise ISPError(r)
        return r

    def enter_isp(self, delay=0.01):
        """Enter ISP mode by controlling the DTR (/RST) and RTS (/ISP) lines

        This operation is performed synchronously, with delays.
        """
        self._uart.rts = True
        time.sleep(delay)
        self._uart.dtr = True
        time.sleep(delay)
        self._uart.dtr = False
        time.sleep(delay)
        self._uart.rts = False

    def synchronize(self, verbose=False, max_tries=None):
        """Begin communication with the microcontroller

        If verbose is True, prints a . for every synchronization attempt.
        If max_tries is an integer, attempt to synchronize at most that many
        times before failing by raising RecvTimeout.
        """
        # Synchronize with the MCU
        while True:
            # Send a ?
            self._uart.write(b"?")
            self._uart.flush()
            if verbose:
                print(".", end="", flush=True)
            # Receive a response
            try:
                s = self._readline()
            except RecvTimeout:
                if max_tries is not None:
                    max_tries -= 1
                    if max_tries <= 0:
                        raise
                continue
            # If we got the right response, break
            if s == b"Synchronized\r\n":
                break
        # Tell the MCU we've synchronized
        s = self._send_command_raw(b"Synchronized\r\n")
        # Next, it should say OK, at which point we're done synchronizing
        if s != b"OK\r\n":
            raise ISPError("Wrong response during synchronization")

        # Send clock frequency in kHz
        s = self._send_command_raw("{:d}\r\n".format(self._clock).encode(
            "utf-8"))
        # Next, it should say OK
        if s != b"OK\r\n":
            raise ISPError("Wrong response during synchronization")

    def close(self):
        """Close the serial port"""
        self._uart.close()

    def unlock(self, code="23130"):
        """Unlock the flash write, erase, and go commands"""
        self._send_command("U {}\r\n".format(code).encode("utf-8"))

    @property
    def baudrate(self):
        """The baud rate used for communication"""
        return self._uart.baudrate

    @baudrate.setter
    def baudrate(self, br):
        self._send_command("B {} {}\r\n".format(br,
            self._uart.stopbits).encode("utf-8"))
        # Update the baud rate for our UART
        self._uart.baudrate = br

    @property
    def stopbits(self):
        """The number of stop bits used for communication"""
        return self._uart.stopbits

    @stopbits.setter
    def stopbits(self, sb):
        self._send_command("B {} {}\r\n".format(self._uart.baudrate,
            sb).encode("utf-8"))
        # Update the number of stop bits for our UART
        self._uart.stopbits = sb

    @property
    def echo(self):
        """Whether the microcontroller echoes characters back to the host"""
        return self._echo

    @echo.setter
    def echo(self, setting):
        setting = bool(setting)
        self._send_command("A {}\r\n".format(int(setting)).encode("utf-8"))
        self._echo = setting

    def write_ram(self, start, data, count=None):
        """Write count bytes from data to RAM at the given start address

        Start and count must be multiples of four.  If count is not specified,
        len(data) is used.
        """
        # Get the length of the data we're writing
        if count is None:
            count = len(data)
        # Ask to write data
        self._send_command("W {} {}\r\n".format(start, count).encode("utf-8"))
        # Send the data
        # NOTE: this is right for LPC8xx chips, not others
        self._writeline(data[:count], plain=True)
        return

    def read_memory(self, start, count):
        """Read count bytes starting at the given address

        Start and count must be multiples of four.
        """
        self._send_command("R {} {}\r\n".format(start, count).encode("utf-8"))
        return self._uart.read(count)

    def prepare_write(self, start=None, end=None):
        """Prepare the the given flash sector(s) for write operations

        If end is not specified, only the start sector is prepared.
        If neither start nor end is specified, prepares all flash sectors.
        """
        if start is None and end is None:
            start = 0
            end = len(self._chip.sectors) - 1
        elif end is None:
            end = start
        self._send_command("P {} {}\r\n".format(start, end).encode("utf-8"))

    def copy_ram_to_flash(self, flash, ram, count):
        """Copy count bytes from RAM to flash

        The flash address should be a 64 byte boundary.  Count should be a
        power of two in [64, 1024].
        """
        self._send_command("C {} {} {}\r\n".format(flash, ram, count).encode(
            "utf-8"))

    def go(self, address=0, mode="T"):
        """Jump to the given address, in the given mode of execution

        Of course, this function generally causes the ISP command handler to
        stop running, so it is typically appropriate to follow this with a call
        to LPC.close.
        """
        self._writeline("G {} {}\r\n".format(address, mode).encode("utf-8"))

    def erase(self, start=None, end=None):
        """Erase the given flash sector(s)

        If end is not specified, only the start sector is erased.
        If neither start nor end is specified, erases all flash sectors.
        """
        if start is None and end is None:
            start = 0
            end = len(self._chip.sectors) - 1
        elif end is None:
            end = start
        self._send_command("E {} {}\r\n".format(start, end).encode("utf-8"))

    def blank_check(self, start, end=None):
        """Check if the given flash sectors are blank

        If end is not specified, only the start sector is checked.

        Returns None if the sector is blank, or a tuple containing the offset
        and value of the first non-blank word location if the sector is not
        blank.  If CRP is enabled, the offset and value are always reported as
        zero.
        """
        if end is None:
            end = start
        try:
            self._send_command("I {} {}\r\n".format(start, end).encode(
                "utf-8"))
        except ISPError as e:
            # Return a tuple for SECTOR_NOT_BLANK
            if e.args[0] == ReturnCode.SECTOR_NOT_BLANK:
                offset = int(self._readline())
                value = int(self._readline())
                return (offset, value)
            raise

    @property
    def part_id(self):
        """The identification number for the part"""
        self._send_command(b"J\r\n")
        return int(self._readline())

    @property
    def boot_code_version(self):
        """The boot code version number (major, minor)"""
        self._send_command(b"K\r\n")
        major = int(self._readline())
        minor = int(self._readline())
        return (major, minor)

    def compare(self, addr1, addr2, count):
        """Compart count bytes starting from the two addresses

        Both addresses should be on word boundaries, and count should be a
        multiple of four.

        Returns None if the two blocks are equal, or the byte offset of the
        first mismatched word if they are not.
        """
        try:
            self._send_command("M {} {} {}\r\n".format(addr1, addr2,
                count).encode("utf-8"))
        except ISPError as e:
            # Return an offset for COMPARE_ERROR
            if e.args[0] == ReturnCode.COMPARE_ERROR:
                return int(self._readline())
            raise

    @property
    def uid(self):
        """The microcontroller's unique ID, as bytes"""
        self._send_command(b"N\r\n")
        words = []
        for _ in range(4):
            words.append(int(self._readline()))
        return struct.pack("<4I", *words)

    def read_crc32(self, start, count):
        """Compute the CRC checksum of a black of RAM or flash

        Start must be on a word boundary, and count must be a multiple of four.
        """
        self._send_command("S {} {}\r\n".format(start, count).encode("utf-8"))
        return int(self._readline())

    def flash_hex(self, ihex, verbose=False):
        """Write an IntelHex object to flash

        Only the sectors that have any data in ihex are changed.  These sectors
        are erased and written with the new data, destroying anything that was
        in the sector before.
        """
        # Assert that we have enough RAM to hold the largest flash sector
        assert (((self._chip.ram_start + 0x400*self._chip.ram)
                - self._chip.ram_base) >= max(self._chip.sectors))
        # Assert that the largest sector is no larger than max_copy
        assert (self._chip.max_copy >= max(self._chip.sectors))
        # NOTE: of course both of these assertions wouldn't be necessary if we
        # were more careful below, but for the chips I'm using they hold, so
        # I'm in no rush to make this perfect.

        # Get the sectors we're rewriting
        sectors_used = self._chip.sectors_used(ihex.segments())

        # Erase the sectors that aren't already blank
        for sector in sectors_used:
            if self.blank_check(sector) is not None:
                if verbose:
                    print("Erasing sector {}".format(sector))
                self.prepare_write(sector)
                self.erase(sector)

        # Write sectors, with 0 at the end
        ss = self._chip.sector_segments
        if 0 in sectors_used:
            sectors_used.remove(0)
            sectors_used.append(0)
        for sector in sectors_used:
            if verbose:
                print("Writing sector {}".format(sector))
            # Get the data we'll be writing
            secdat = ihex.tobinstr(start=ss[sector][0], end=ss[sector][1]-1)

            # If we're writing sector 0, set the checksum
            if sector == 0:
                iv = struct.unpack('<7I', secdat[0:28])
                cs = struct.pack('<I', (-(sum(iv) % 2**32)) & 0xFFFFFFFF)
                secdat = secdat[:28] + cs + secdat[32:]

            # Write data to RAM
            bs = 0x100
            for i in range(0, len(secdat), bs):
                self.write_ram(self._chip.ram_base+i, secdat[i:i+bs])

            # Copy RAM to flash
            self.prepare_write(sector)
            self.copy_ram_to_flash(ss[sector][0], self._chip.ram_base,
                    len(secdat))

    def verify(self, ihex, verbose=False):
        """Verify that the data in an IntelHex object is stored in flash"""
        # Get the sectors we're verifying
        sectors_used = self._chip.sectors_used(ihex.segments())

        # Verify segments
        ss = self._chip.sector_segments
        for sector in sectors_used:
            if verbose:
                print("Verifying sector {}... ".format(sector), end="")
            # Get the data we're verifying
            secdat = ihex.tobinstr(start=ss[sector][0], end=ss[sector][1]-1)

            # Read data from flash
            try:
                flash = self.read_memory(ss[sector][0],
                        self._chip.sectors[sector])
            except ISPError as e:
                if e.args[0] == ReturnCode.CODE_READ_PROTECTION_ENABLED:
                    print()
                raise

            # Verify the sector
            if sector == 0:
                # Avoid comparing first 64 bytes of sector 0 because these are
                # remapped to flash boot sector
                secdat = secdat[64:]
                flash = flash[64:]
            if secdat != flash:
                print("failed!")
                raise ISPError("Flash verification failed")
            else:
                print()


class LPC8xx(LPC):
    """Interface for LPC8xx in-system programming"""

    def __init__(self, lpc, chip):
        """Initialize an LPC8xx from an existing LPC object"""
        super().__init__(lpc)
        self._chip = chip


class ReturnCode(Enum):
    """LPC ISP return codes

    From UM10800, section 25.6.1.16.
    """
    CMD_SUCCESS = 0
    INVALID_COMMAND = 1
    SRC_ADDR_ERROR = 2
    DST_ADDR_ERROR = 3
    SRC_ADDR_NOT_MAPPED = 4
    DST_ADDR_NOT_MAPPED = 5
    COUNT_ERROR = 6
    INVALID_SECTOR = 7
    SECTOR_NOT_BLANK = 8
    SECTOR_NOT_PREPARED_FOR_WRITE_OPERATION = 9
    COMPARE_ERROR = 10
    BUSY = 11
    PARAM_ERROR = 12
    ADDR_ERROR = 13
    ADDR_NOT_MAPPED = 14
    CMD_LOCKED = 15
    INVALID_CODE = 16
    INVALID_BAUD_RATE = 17
    INVALID_STOP_BIT = 18
    CODE_READ_PROTECTION_ENABLED = 19
