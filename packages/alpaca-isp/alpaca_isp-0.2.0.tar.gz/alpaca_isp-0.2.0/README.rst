Alpaca ISP
==========

In-system programming tool for LPC microcontrollers

Features
--------

-  Provides a Pythonic interface to the LPC ISP command handler
-  Can put microcontrollers into ISP mode by manipulating the serial port's DTR
   (/RST) and RTS (/ISP) lines
-  Convenient command-line interface for flashing from build systems

Requirements
------------

-  Python 3.6 (probably works with older versions of Python 3, but untested)
-  PySerial >= 3.4
-  IntelHex >= 2.1
