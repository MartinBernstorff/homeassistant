import appdaemon.appapi as appapi
import time
import datetime

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

class CircadianSingleLights(appapi.AppDaemon):

    def initialize(self):
        self.log("Initializing carpe diem with switch: " + self.args["switch"])

        #Setup the switch object
        switch = self.args["switch"]

        time = datetime.time(21, 15, 0)
        self.run_daily(self.ceiling, time)

    def ceiling(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state(switch) == "on":
            self.turn_off("light.loft")
