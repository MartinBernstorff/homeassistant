import appdaemon.appapi as appapi
import datetime
import time
import carpediem

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
        #Initiate switch object
        self.switch = self.args["switch"]

        self.log("Sunset initialized")
        hour = int(self.args["hour"])
        minute = int(self.args["minute"])

        self.sunsettime = datetime.time(hour, minute, 0)

        self.log("I'll make sure you get to sleep at the right time by starting sunset at {}".format(self.sunsettime))

        # Schedule a daily callback that will start sunset at sunsettime
        self.run_daily(self.sunsetmonitor, self.sunsettime)
        self.run_daily(self.sunsetreol, self.sunsettime)
        self.run_daily(self.sunsetceiling, self.sunsettime)

        #Reset the switch at 08:00 each day
        time = datetime.time(8, 0, 0)
        self.run_daily(self.reset, time)

        #Turn on sunset switch at init
        self.turn_on(self.switch)

        #Update factor
        self.updatefactor()
        self.listen_state(self.updatefactor, self.args["factor"])

    def sunsetmonitor(self, entity, attribute, old, new, kwargs):
        if self.get_state(self.switch) == "on":
            light = "light.monitor"
            self.setstate(light, 50, 1800)
            self.setstate(light, 40, 10, [ 0.674, 0.322 ])

    def sunsetceiling(self, entity, attribute, old, new, kwargs):
        if self.get_state(self.switch) == "on":
            light = "light.loft"
            self.setstate(light, 0, 300)
            self.turn_off(light)

    def sunsetreol(self, entity, attribute, old, new, kwargs):
        if self.get_state(self.switch) == "on":
            light = "light.reol"
            self.setstate(light, 150, 1800)
            self.turn_off(light)

    def setstate(self, lt, bness, fade, color=""):
        # Only change state if the light is on and the sunset switch is on
        if self.get_state(self.switch) == "on" and self.get_state(lt) == "on":
            self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s")

            if color != "":
                self.turn_on(lt, brightness = bness, transition = self.modulator * fade, xy_color = color)
            else:
                self.turn_on(lt, brightness = bness, transition = self.modulator * fade)


            time.sleep(self.modulator * fade)
        else:
            self.log("Switch turned off, terminating")

    def updatefactor(self, entity="", attribute="", old="", new="", kwargs=""):
        self.factor_state = self.get_state(self.args["factor"])

        if self.factor_state == "50%":
            self.modulator = 0.01
        elif self.factor_state == "75%":
            self.modulator = 0.75
        elif self.factor_state == "100%":
            self.modulator = 1
        elif self.factor_state == "125%":
            self.modulator = 1.25

        self.log("Modulator set to " + str(self.modulator))

    def reset(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_on(self.args["switch"])
