# -*- coding: utf-8 -*-
"""
SMFSWmath.py
Author: SMFSW
Copyright (c) 2016-2017 SMFSW

The MIT License (MIT)
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from math import pi


def rad2deg(radians):
    """ Radians to Degrees
    :param radians: value to convert in radians
    :return: value in degrees """
    degrees = 180 * radians / pi
    return degrees


def deg2rad(degrees):
    """ Degrees to Radians
    :param degrees: value to convert in deg
    :return: value in radians """
    radians = pi * degrees / 180
    return radians


def percent(val, val_max):
    """ Percentage calc
    :param val: value
    :param val_max: max value
    :return: ratio in percentage """
    return float(val * 100) / val_max


def scale(val, old_scale, new_scale=100):
    """ Change scale of a value
    :param val: value
    :param old_scale: current scale max value
    :param new_scale: new scale max value
    :return: value converted to new scale """
    return float(val * new_scale) / old_scale


if __name__ == "__main__":
    print(rad2deg(pi))
    print(deg2rad(180))
    print(percent(150, 255))
    print(percent(3, 10))
    print(scale(150, 255))      # idem percent
    print(scale(3, 10, 2048))
