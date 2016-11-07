import appdaemon.appapi as appapi
import circadian_gen
import datetime
from multiprocessing import Process

#
# Circadian app
#
# Args:
#   None atm

class CircadianSetter(appapi.AppDaemon):

    def initialize(self):
        #Get current time and small time delta to initiate run_every
        self.now = datetime.datetime.now()
        b = self.now + datetime.timedelta(0, 3)

        self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
        self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)

        self.log("{} initiated".format(__name__))

        #Run every 2 minutes
        self.run_every(self.setlights, b, 120)
        self.listen_state(self.setlights, "input_boolean.circadian", new = "on")
        self.listen_state(self.setlights_quick, "light.monitor", new = "on", old = "off")
        self.listen_state(self.set_toilet, "light.bathroom", new = "on", old = "off")

    def setlights(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on":
            self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
            self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)
            self.now = datetime.datetime.now()

            self.setlight("light.monitor", 30, 1.4)
            self.setlight("light.reol", 30, 0.4)
            self.setlight("light.loft", 30, 0.6)

            #self.log("Updating lights, time is {}, color temp is {} and brightness is {}".format(self.now.time(), self.hue, self.brightness))

        else:
            self.log("Circadian switch is off, lights not updated")

    def setlights_quick(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on":
            self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
            self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)
            self.now = datetime.datetime.now()

            self.setlight("light.monitor", 2, 1.4)
            self.setlight("light.reol", 2, 0.4)
            self.setlight("light.loft", 2, 0.6)
            self.setlight("light.bathroom", 2, 1.4)

            #self.log("Updating lights, time is {}, color temp is {} and brightness is {}".format(self.now.time(), self.hue, self.brightness))

        else:
            self.log("Circadian switch is off, lights not updated")

    def set_toilet(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on":
            self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
            self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)
            self.now = datetime.datetime.now()

            self.setlight("light.bathroom", 1, 1.4)


    def setlight(self, light, transition, modifier):
        if self.get_state("input_boolean.circadian") == "on":
            if self.get_state(light) == "on":
                self.turn_on(light, transition = transition, xy_color = circadian_gen.CircadianGen.get_circ_hue(self), brightness = modifier * circadian_gen.CircadianGen.get_circ_brightness(self))
