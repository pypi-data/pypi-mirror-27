# -*- coding: utf-8 -*-
"""
SMFSWvect.py
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

from math import sqrt, radians, cos, sin


# noinspection PyPep8Naming
class vect(object):
    """ Simple vector class (always originating from 0,0) with arithmetics """
    def __init__(self, x, y):
        """ Init vector with x, y values """
        self.x = x
        self.y = y

    def __repr__(self):
        """ :return: tuple of x, y coords from self """
        return self.x, self.y

    def __str__(self):
        """ :return: string x, y coords of tuple from self """
        # return "X: {} - Y: {}".format(self.x, self.y)
        return "({}, {})".format(self.x, self.y)

    def __getitem__(self, item):
        """ get item value from self
        :param item: index in array
        :return: index corresponding value """
        try:
            assert item < 2
        except AssertionError:
            print("Requested item is outside the vector")
            return 0
        else:
            if item == 0:
                return self.x
            else:
                return self.y

    def __setitem__(self, item, val):
        """ Set item in self """
        try:
            assert item < 2
        except AssertionError:
            print("Would store value outside the vector")
            return 0
        else:
            if item == 0:
                self.x = val
            else:
                self.y = val
            return val

    def __add__(self, vect2):
        """ Add vect with a value or other vect
        :param vect2: can be value to add vector with or other vector x, y coords
        :return: added self """
        if isinstance(vect2, vect):
            self.x += vect2.x
            self.y += vect2.y
        elif isinstance(vect2, int) or isinstance(vect2, float):
            self.x += vect2
            self.y += vect2

        return self

    def __iadd__(self, vect2):
        """ Augmented add vect with a value or other vect
        :param vect2: can be value to add vector with or other vector x, y coords
        :return: added self """
        if isinstance(vect2, vect):
            self.x += vect2.x
            self.y += vect2.y
        elif isinstance(vect2, int) or isinstance(vect2, float):
            self.x += vect2
            self.y += vect2

        return self

    def add(self, vect2):
        """ Add vect2 vector to self (same as __add__ but returns nothing)
        :param vect2: vect2 x, y coords to add """
        self.x += vect2.x
        self.y += vect2.y

    def __sub__(self, vect2):
        """ Substract vect with a value or other vect
        :param vect2: can be value to substract vector with or other vector x, y coords
        :return: subtracted self """
        if isinstance(vect2, vect):
            self.x -= vect2.x
            self.y -= vect2.y
        elif isinstance(vect2, int) or isinstance(vect2, float):
            self.x -= vect2
            self.y -= vect2

        return self

    def __isub__(self, vect2):
        """ Augmented substract vect with a value (not very relevant) or other vect
        :param vect2: can be value to substract vector with or other vector x, y coords
        :return: subtracted self """
        if isinstance(vect2, vect):
            self.x -= vect2.x
            self.y -= vect2.y
        elif isinstance(vect2, int) or isinstance(vect2, float):
            self.x -= vect2
            self.y -= vect2

        return self

    def sub(self, vect2):
        """ Substract vect2 vector to self (same as __sub__ but returns nothing)
        :param vect2: vect2 x, y coords to substract """
        self.x -= vect2.x
        self.y -= vect2.y

    def __mul__(self, vect2):
        """ Multiply vect with a value or other vect
        :param vect2: can be value to multiply vector with or other vector x, y coords
        :return: multiplied self """
        if isinstance(vect2, vect):
            self.x *= vect2.x
            self.y *= vect2.y
        elif isinstance(vect2, int) or isinstance(vect2, float):
            self.x *= vect2
            self.y *= vect2

        return self

    def __imul__(self, vect2):
        """ Augmented multiply vect with a coef or other vect
        :param vect2: can be coef to multiply with or other vector x, y coords
        :return: multiplied self """
        if isinstance(vect2, vect):
            self.x *= vect2.x
            self.y *= vect2.y
        elif isinstance(vect2, int) or isinstance(vect2, float):
            self.x *= vect2
            self.y *= vect2

        return self

    def mul(self, number):
        """ Multiply vect with a coef (same as __mul__ but returns nothing)
        :param number: coef to multiply with """
        self.x *= number
        self.y *= number

    def __div__(self, vect2):   # works with Python 3, but not with Python 2 when using __truediv__
        """ Divide vect with a value or other vect
        :param vect2: can be value to divide vector with or other vector x, y coords
        :return: divided self """
        try:
            if isinstance(vect2, vect):
                self.x /= vect2.x
                self.y /= vect2.y
            elif isinstance(vect2, int) or isinstance(vect2, float):
                self.x /= vect2
                self.y /= vect2
        except ZeroDivisionError:
            pass

        return self

    def __itruediv__(self, vect2):  # __itruediv__ used for compatibility with Python3
        """ Augmented divide vect with a coef or other vect
        :param vect2: can be coef to divide with or other vector x, y coords
        :return: divided self """
        if isinstance(vect2, vect):
            if vect2.x != 0 and vect2.y != 0:
                self.x /= vect2.x
                self.y /= vect2.y
        elif isinstance(vect2, int) or isinstance(vect2, float):
            if vect2 != 0:
                self.x /= vect2
                self.y /= vect2

        return self

    def div(self, number):
        """ Divide vect with a coef (same as __div__ but returns nothing)
        :param number: coef to divide with """
        if number != 0:
            self.x /= number
            self.y /= number

    def rotate(self, angle):
        """ Rotate vect with given angle
        :param angle: rotation angle (in degrees)
        :return: rotated self """
        rad = radians(angle)
        tmp_x = self.x
        tmp_y = self.y
        self.x = round((tmp_x * cos(rad)) - (tmp_y * sin(rad)), 3)
        self.y = round((tmp_x * sin(rad)) + (tmp_y * cos(rad)), 3)
        del rad, tmp_x, tmp_y
        return self

    def equals(self, vect2):
        """ Tests if given vect2 vector is equal to self
        :param vect2: vect2 x, y coords to compare with
        :return: True if equals, False otherwise """
        if self.x == vect2.x and self.y == vect2.y:
            return True
        else:
            return False

    def copy(self):
        """ :return: Returns a new instance of self """
        return vect(self.x, self.y)

    def len(self):
        """ :return: computed length from self """
        return sqrt((self.x ** 2) + (self.y ** 2))

    def getx(self):
        """ :return: x value from self """
        return self.x

    def gety(self):
        """ :return: y value from self """
        return self.y

    def get_vect(self):
        """ :return: tuple of x,y coords from self """
        return self.x, self.y


if __name__ == "__main__":
    v1 = vect(50, 20)
    v2 = vect(100, 10)

    v1.add(v2)
    print("add vectors: {}".format(v1))
    v2.mul(2)
    print("mul 2nd vector: {}".format(v2))
    v1.sub(v2)
    print("sub vectors: {}".format(v1))
    v1.div(2)
    print("div 1st vector: {}".format(v1))

    v1 += v2
    print("add vectors: {}".format(v1))
    v1 = v1 + v2
    print("add vectors: {}".format(v1))
    v2 = v2 + 10
    print("add 10 to 2nd vector: {}".format(v2))
    v2 = v2 - 10
    print("sub 10 to 2nd vector: {}".format(v2))

    v2 -= v1
    print("sub vectors in v2: {}".format(v2))

    v2 /= 0
    print("tst div 0 on v2: {}".format(v2))

    v3 = vect(100, 10)
    v3.rotate(90)
    print("rotate vect v3: {}".format(v3))
