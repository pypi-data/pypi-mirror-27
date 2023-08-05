# -*- coding: utf-8 -*-
"""
SMFSWunittst.py
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

import time


def timetst(nbsec=0):
    """ Adds test report
    :param nbsec: elapsed time before printing a message
    :return: timetst decorator """
    def decor(fct):
        """
        :param fct: function to decorate with time test
        :return: decorator """
        def decfct():
            """ :return: decorated function """
            string = str()
            tim = time.ctime()
            string += "\nStarted {}".format(tim)
            time_bef = time.time()
            retval = fct()
            time_aft = time.time()
            time_exec = time_aft - time_bef
            if time_exec >= nbsec:
                string += "\nelapsed time: {} s for function {}".format(time_exec, fct)
                string += "\naverage time by case: %.03f µs" % ((time_exec / retval) * 1000000)
                string += "\n--- TST END ---\n"
            return string
        return decfct
    return decor


class RandPickInRange(object):
    """ Random number compare class """
    def __init__(self, rng_dwn, rng_up):
        """
        :param rng_dwn: random limit down
        :param rng_up: random limit up """
        self.cpt = 0
        self.up = rng_up
        self.down = rng_dwn
        self.nxt = self.reroll()

    def reroll(self):
        """ generates a new number, and stores it to nxt
        :return: return new nxt value """
        import random
        self.nxt = random.randint(self.down, self.up)
        return self.nxt

    def increment(self):
        """ increments cpt for compare
        :return: return actual cpt value """
        self.cpt += 1
        return self.cpt

    def restart(self):
        """ reset count cpt and reroll
        :return: return new nxt value """
        self.cpt = 0
        return self.reroll()

    def compare(self):
        """ compare cpt with nxt
        :return: return True if cpt overflows """
        if self.cpt > self.nxt:
            return True
        else:
            return False


def choice(tst):
    """ dict lookup
    :param tst: value to test for function choose
    :return: name of the function to call (to affect to a var first, then call through var() """
    try:
        # asserting value for exception catching
        assert tst >= 0
        assert tst <= 1
        return {
            # do not use (), otherwise each func is executed while looking up in the table
            0: fc1,
            1: fc2,
        }[tst]
    except AssertionError:
        print("function id not in range")


def fc1():
    """ Test function 1 """
    print("fc1")


def fc2():
    """ Test function 2 """
    print("fc2")


if __name__ == "__main__":
    @timetst()
    def iter_func():
        j = 0
        for i in range(10000):
            j += int(i/2)

        print("Computed value: {}".format(j))
        return i

    print(iter_func())

    fc = choice(1)
    fc()

    print("")
