import appdaemon.appapi as appapi
import datetime
import time

#
# Circadian_schedular app
#
# Args:
# automation (switch that needs to be turned on/off)
#

class CircadianScheduler(appapi.AppDaemon):

    def initialize(self):
        self.log("Circadian_schedular initiated")

        time = datetime.time(7, 30, 0)
        time2 = datetime.time(22, 0, 0)
        self.log(time)

        # Schedule a daily callback that will call run_daily() at 12am every midday
        self.run_daily(self.CircadianOn, time)
        self.run_daily(self.CircadianOff, time2)

    def CircadianOn(self, kwargs):
        self.turn_on("input_boolean.circadian")
        self.log("Turned on circadian")

    def CircadianOff(self, kwargs):
        self.turn_off("input_boolean.circadian")
        self.log("Turned off circadian")
