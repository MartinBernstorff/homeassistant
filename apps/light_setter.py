import appdaemon.appapi as appapi
import circadian_gen
import datetime
import time

#
# Circadian app
#
# Args:
#   None atm

class LightSetter(appapi.AppDaemon):

    def initialize(self):
        #Get current time and small time delta to initiate run_every
        self.now = datetime.datetime.now()
        b = self.now + datetime.timedelta(0, 3)

        self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
        self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)

        self.log("Lightsetter initiated")

        #Run every 30 seconds
        self.run_every(self.setlights, b, 60)
        self.listen_state(self.setlights, "input_boolean.circadian", new = "on")

    def setlights(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on":
            self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
            self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)
            self.now = datetime.datetime.now()
            self.log("Updating lights, time is {}, color temp is {} and brightness is {}".format(self.now.time(), self.hue, self.brightness))

            self.setlight("light.monitor", 1.2)
            self.setlight("light.reol", 0.8)
            self.setlight("light.loft", 1)

        else:
            self.log("Circadian switch is off, lights not updated")

    def setlight(self, light, modifier):
        if self.get_state("input_boolean.circadian") == "on":
            if self.get_state(light) == "on":
                self.turn_on(light, transition = 1, xy_color = circadian_gen.CircadianGen.get_circ_hue(self), brightness = modifier * circadian_gen.CircadianGen.get_circ_brightness(self))
