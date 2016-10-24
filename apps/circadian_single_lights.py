import appdaemon.appapi as appapi
import time
import datetime

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script

class CircadianSingleLights(appapi.AppDaemon):

    def initialize(self):
        self.log("Initializing CircadianSingleLights with switch: " + self.args["switch"])

        #Setup the switch object
        switch = self.args["switch"]

        #Setup callback
        time = datetime.time(21, 16, 0)
        self.run_daily(self.ceiling, time)

    def ceiling(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state(self.args["switch"]) == "on":
            self.turn_off("light.loft")
