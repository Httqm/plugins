#!/usr/bin/env python

class Debug(object):

    def __init__(self):
        self._mySys = __import__('sys')
        self._show  = False


    def enable(self, param):
        self._show = True if param else False


    def die(self, params):
        """ Display an error message and leave the program. """
        print (params['exitMessage'])
        self._mySys.exit(2)


    def show(self, message):
        if self._show:
            import inspect
            print ("\n" \
                + " ++=================== DEBUG =========================\n" \
                + ' || FILE    : ' + str(inspect.stack()[1][1]) + "\n" \
                + ' || LINE    : ' + str(inspect.stack()[1][2]) + "\n" \
                + ' || CALLER  : ' + str(inspect.stack()[1][3]) + "\n" \
                + ' || MESSAGE : ' + str(message) + "\n" \
                + " ++================== /DEBUG =========================\n")

