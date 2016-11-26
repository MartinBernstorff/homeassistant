import appdaemon.appapi as appapi
import circadian_gen
import datetime
import time
import shelve

#
# Circadian app
#
# Args:
#   None atm

class Tester(appapi.AppDaemon):
    def initialize(self):

        #Get hue values
        self.device_db = shelve.open("/etc/appdaemon/circadian.db")
        circ_brightness = self.device_db["brightness"]
        circ_hue = self.device_db["hue"]

        self.log("Brightness is {}".format(circ_brightness))
        self.log("Hue is {}".format(circ_hue))


        """
        #Test with simulated time
        self.now = datetime.datetime.now()
        self.now = self.now.replace(hour=7, minute=0, second=0)
        self.log("Simulated time is {}".format(self.now.time()))
        self.log("Color temp is {}".format(circadian_gen.CircadianGen.get_circ_hue(self)))
        self.log("Brightness is {}".format(circadian_gen.CircadianGen.get_circ_brightness(self)))
        """
