#!/usr/bin/env python

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
