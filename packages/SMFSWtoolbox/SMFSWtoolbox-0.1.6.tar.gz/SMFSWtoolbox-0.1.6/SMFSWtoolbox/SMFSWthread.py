# -*- coding: utf-8 -*-
"""
SMFSWthread.py
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

from time import sleep
import threading


class StoppableThread(threading.Thread):
    """ Init super class StoppableThread """
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        """ stop running thread """
        if self.isAlive() is True:
            self.stop_event.set()   # set event to signal thread to terminate
            self.join()             # block calling thread until thread really has terminated


class TimedAction(StoppableThread):
    """ Timed Action class """
    def __init__(self, interval, function):
        super(TimedAction, self).__init__()     # init subclasses
        self._interval = interval
        self._function = function

    def run(self):
        """ thread running until triggered to stop """
        while not self.stop_event.is_set():
            self._function()
            sleep(self._interval)


# @staticmethod
def timed_act(interval, function, iterations=0):
    """ Make periodic call to function
    :param interval: period (in seconds)
    :param function: function to call
    :param iterations: nb of iterations
    :return: called function return value """
    if iterations != 1:
        threading.Timer(interval, timed_act, [interval, function, 0 if iterations == 0 else iterations - 1]).start()
    return function()


if __name__ == "__main__":
    import time

    def tim_func():
        print("{} called at: {}".format(tim_func, time.clock()))

    def tim_func2():
        print("{} called at: {}".format(tim_func2, time.clock()))

    def tim_class():
        print("{} called at: {}".format(tim_class, time.clock()))

    timed_act(0.750, tim_func)
    timed_act(0.450, tim_func2)

    tim = TimedAction(2, tim_class)
    tim.start()
    time.sleep(30)
    tim.stop()

    # note that tim_func & tim_func2 keeps running
