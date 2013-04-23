#!/usr/bin/env python3

######################################### url.py ####################################################
# FUNCTION :
#
# AUTHOR :	Matthieu FOURNET (fournet.matthieu@gmail.com)
# LICENSE :	GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :	1.
#
########################################## ##########################################################


import re


class Url(object):

    def __init__(self, full):
        self._full = full


    def getFullUrl(self):
        return self._full


    def getQuery(self):
        tmp = self._full.replace('http://' + self.getHostName(), '')
        return tmp if len(tmp) else '/'


    def getHostName(self):
        match = re.search('^http://([^:/]*)(:|/)?.*$', self._full)   # TODO : should start with 'http....', no leading space allowed
        # http://docs.python.org/howto/regex#performing-matches
        if match:
            return match.group(1)
        else:
            return self._full
