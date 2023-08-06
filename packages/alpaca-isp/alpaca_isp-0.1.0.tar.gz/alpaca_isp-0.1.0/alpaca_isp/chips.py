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
"""Chips supported by Alpaca ISP"""

from collections import namedtuple

from alpaca_isp.lpc import LPC8xx


class Chip(namedtuple("Chip", [
        # Name of the chip
        "name",
        # Class that represents this chip
        "family",
        # Size of flash in KiB
        "flash",
        # Size of RAM in KiB
        "ram",
        # Address of the start of RAM
        "ram_start",
        # RAM location to which we can safely write
        "ram_base",
        # Maximum number of bytes we can copy
        "max_copy",
        # Sector table
        "sectors"])):
    __slots__ = ()

    @property
    def sector_segments(self):
        """Returns a list of (start, end) tuples for each flash sector"""
        sector_segments = []
        for i in range(len(self.sectors)):
            sector_segments.append((sum(self.sectors[:i]),
                sum(self.sectors[:i+1])))

        return sector_segments

    def sectors_used(self, segments):
        """Returns a list of sectors used by the given memory segments

        segments: a list of (start, end) tuples representing segments of used
            memory
        """
        sector_segments = self.sector_segments

        s = set()
        for dseg in segments:
            for i, sseg in enumerate(sector_segments):
                if ((dseg[0] >= sseg[0] and dseg[1] <= sseg[1])
                        or (dseg[0] < sseg[0] and dseg[1] > sseg[1])
                        or (sseg[0] <= dseg[0] < sseg[1])
                        or (sseg[0] < dseg[1] <= sseg[1])):
                    s.add(i)

        return sorted(s)


chips = {
    0x00008221: Chip(
        name="LPC822M101JHI33",
        family=LPC8xx,
        flash=16,
        ram=4,
        ram_start=0x10000000,
        ram_base=0x10000300,
        max_copy=1024,
        sectors=(1024,)*16),
    0x00008222: Chip(
        name="LPC822M101JDH20",
        family=LPC8xx,
        flash=16,
        ram=4,
        ram_start=0x10000000,
        ram_base=0x10000300,
        max_copy=1024,
        sectors=(1024,)*16),
    0x00008241: Chip(
        name="LPC824M201JHI33",
        family=LPC8xx,
        flash=32,
        ram=8,
        ram_start=0x10000000,
        ram_base=0x10000300,
        max_copy=1024,
        sectors=(1024,)*32),
    0x00008242: Chip(
        name="LPC824M201JDH20",
        family=LPC8xx,
        flash=32,
        ram=8,
        ram_start=0x10000000,
        ram_base=0x10000300,
        max_copy=1024,
        sectors=(1024,)*32)
}
