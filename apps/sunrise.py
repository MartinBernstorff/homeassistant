import appdaemon.appapi as appapi
import time
import datetime

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   light: The light that's used for sunrise

class Sunrise(appapi.AppDaemon):

    def initialize(self):
        self.log("Initializing sunrise")

        #Setup the switch object
        switch = self.args["switch"]
        self.update_time()
        self.listen_state(self.update_time, "input_select.sunrise_hour")
        self.listen_state(self.update_time, "input_select.sunrise_minute")

        #Set sunrise time


    def rise(self, entity="", attribute="", old="", new="", kwargs=""):
        #Make short corner light var
        self.modulator = 1
        self.turn_off("input_boolean.circadian")
        self.setstate("light.monitor", 1, 1, [ 0.674, 0.322 ], 3600)
        self.setstate("light.monitor", 100, 1800, [ 0.5268, 0.4133 ])
        self.turn_on("input_boolean.circadian")

    def setstate(self="", lt="", bness="", fade="", color="", post_delay="0"):
        switch = self.args["switch"]

        if self.get_state(switch) == "on":
            self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s")

            if color != "":
                self.turn_on(lt, brightness = bness, transition = self.modulator * fade, xy_color = color)
            else:
                self.turn_on(lt, brightness = bness, transition = self.modulator * fade)

            self.log("Sleeping for {}".format(int(self.modulator) * fade + post_delay))
            time.sleep(self.modulator * fade + post_delay)
        else:
            self.log("Switch turned off, terminating")

    def update_time(self, entity="", attribute="", old="", new="", kwargs=""):
        self.hour = self.get_state("input_select.sunrise_hour")
        self.minute = self.get_state("input_select.sunrise_minute")
        self.log("Time set to {}:{}".format(self.hour, self.minute))
        time = datetime.time(int(self.hour), int(self.minute), 0)
        self.cancel_timer(self.sunrise)
        self.sunrise = self.run_daily(self.rise, time)
