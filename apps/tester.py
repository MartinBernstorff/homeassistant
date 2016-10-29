import appdaemon.appapi as appapi
import circadian_gen
import datetime
import time

#
# Circadian app
#
# Args:
#   None atm

class Tester(appapi.AppDaemon):
    def initialize(self):
        """
        self.now = datetime.datetime.now()
        self.now = self.now.replace(hour=7, minute=0, second=0)
        self.log("Simulated time is {}".format(self.now.time()))
        self.log("Color temp is {}".format(circadian_gen.CircadianGen.get_circ_hue(self)))
        self.log("Brightness is {}".format(circadian_gen.CircadianGen.get_circ_brightness(self)))
        """
