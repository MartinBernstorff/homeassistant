import appdaemon.appapi as appapi
import time
import datetime

#
# Carpediem app
#
# Args:
#   switch: The switch that's required for the script to run

class off_scheduler(appapi.AppDaemon):

    def initialize(self):
        switch = self.args["switch"]
        hour = self.args["hour"]
        minute = self.args["minute"]
        entity = self.args["entity"]
        time = datetime.time(int(hour), int(minute), 0)

        self.log("Initializing OffScheduler with switch: {}, {}:{}, {}".format(switch, hour, minute, entity))
        self.run_daily(self.off, time)


    def off(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.args["switch"] is not None:
            if self.get_state(self.args["switch"]):
                self.turn_off(self.args["entity"])
        else:
            self.turn_off(self.args["entity"])
