#!/usr/bin/python3.6


"""
.. module:: binclock
    :platform: Windows, linux
    :synopsis: the entrance point script that launches binary clocks

.. moduleauthor:: Miguel Garcia <zeycus@gmail.com>
"""

import sys

from binary_clock.binclockWrapper import binclock_wrapper


if __name__ == "__main__":
    binclock_wrapper(sys.argv[1:])
