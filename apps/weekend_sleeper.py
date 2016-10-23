import appdaemon.appapi as appapi
import datetime

#
# Weekend_sleeper app
#
# Args:
# automation (switch that needs to be turned on/off)
#

class WeekendSleeper(appapi.AppDaemon):

    def initialize(self):
        self.log("Weekend-sleeper initialized")

        time = datetime.time(12, 0, 0)
        self.log("I'll make sure that you can sleep in by checking the state of input_boolean.sunrise at ")
        self.log(time)

        # Schedule a daily callback that will call run_daily() at 12am every midday
        self.run_daily(self.sleepin, time)

    def sleepin(self, kwargs):
        weekday = datetime.datetime.today().weekday() + 1
        if weekday == 5 or weekday == 6:
            self.turn_off(self.args["automation"])
            self.log("Turned off sunrise to get some sweet sleep")

        if weekday == 7:
            self.turn_on(self.args["automation"])
            self.log("Turned on sunrise to make sure you rise up!")
