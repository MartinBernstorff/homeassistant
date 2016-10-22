import appdaemon.appapi as appapi
import datetime

#
# Weekend_sleeper app
#
# Args:
#

class Sunset(appapi.AppDaemon):

    def initialize(self):
        self.log("Sunset initialized")
        hour = int(self.args["hour"])
        minutes = int(self.args["minutes"])

        time = datetime.nows()

        self.log("I'll make sure that you can sleep in by checking the state of input_boolean.sunrise at ")
        self.log(time)

        # Schedule a daily callback that will call run_daily() at 12am every midday
        self.run_every(self.sunset, time, 30, **kwargs)

    def sunset(self, kwargs):
        self.log("The sun is setting!")
