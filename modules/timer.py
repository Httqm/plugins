#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime


class Timer(object):

#    def __init__(self):
#        self.start()


    def start(self):
        self._startTime = datetime.now()


    def stop(self):
        """ Return the elapsed time as µ-seconds. """
        # source : http://stackoverflow.com/questions/766335/python-speed-testing-time-difference-milliseconds
#        print "START : " + `self._startTime`
#        print "STOP  : " + `self._stopTime`
        duration = datetime.now() - self._startTime     # <== duration is a 'timedelta' object
        return duration.seconds * 1000000 + duration.microseconds

