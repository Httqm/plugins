#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Utility(object):

    def lengthOfLongestKey(self, aDict):
        length = 0
        for key in aDict:
            keyLength   = len(str(key))
            if keyLength > length:
                length = keyLength
        return length


    def computePercentage(self, number, total):
        if total:
            return (number * 1.0) / total * 100
        else:
            return 0


    def isNumber(self, something):
        try:
            float(something)
            return True
        except ValueError:
            return False
