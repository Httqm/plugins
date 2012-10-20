#!/usr/bin/env python

class Debug(object):

    def __init__(self):
        self._mySys = __import__('sys')
        self._show  = False


    def enable(self, enabledByCaller):
        self._show = True if enabledByCaller else False


    def die(self, exitMessage, exitCode=2):
        """
        Display an error message and leave the program.

        The defaut exit code is 2 to identify cases when a script was terminated through this function.
        """
        print (exitMessage)
        self._mySys.exit(exitCode)


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

