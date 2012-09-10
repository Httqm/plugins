#!/usr/bin/env python

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

    def __init__(self, params):
        self._full = params['full']
#        self._clean()


    """
    def _clean(self):
        # http://docs.python.org/library/stdtypes.html#str.rstrip
        self._full = self._full.lstrip().rstrip()
        print 'CLEAN URL : "' + self._full + '"'
    """


    def getFullUrl(self):
        return self._full


    def getQueryUrl(self):
        import string
        tmp = string.replace(self._full, 'http://' + self.getHostName(), '')
        return tmp if len(tmp) else '/'


    def getHostName(self):
        match = re.search('^http://([^:/]*)(:|/)?.*$', self._full)   # TODO : should start with 'http....', no leading space allowed
        # http://docs.python.org/howto/regex#performing-matches
        if match:
            return match.group(1)
        else:
            return self._full
