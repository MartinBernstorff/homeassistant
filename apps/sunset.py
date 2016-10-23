import appdaemon.appapi as appapi
import datetime

#
# Sunset app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length
#   hour: the hour to start sunset
#   minutes: the minutor to start sunset

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

        #Reset the switch at 08:00 each day
        time = datetime.time(8, 0, 0)
        self.run_daily(self.reset, time)

    def sunset(self, kwargs):
        self.log("The sun is setting!")

    def updatefactor(self, entity="", attribute="", old="", new="", kwargs=""):
        self.factor_state = self.get_state(self.args["factor"])

        if self.factor_state == "50%":
            self.modulator = 0.5
        elif self.factor_state == "75%":
            self.modulator = 0.75
        elif self.factor_state == "100%":
            self.modulator = 1
        elif self.factor_state == "125%":
            self.modulator = 1.25

        self.log("Modulator set to " + str(self.modulator))

    def reset(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_off(self.args["switch"])
