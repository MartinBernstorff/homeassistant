import appdaemon.appapi as appapi
import datetime

#
# Circadian app
#
# Args:
#   None atm

class CircadianSetter(appapi.AppDaemon):

    def initialize(self):
        #Get current time and small time delta to initiate run_every
        self.now = self.datetime()
        b = self.now + datetime.timedelta(0, 3)

        self.log("{} initiated".format(__name__))

        #Run every 4 minutes
        self.run_every(self.set_lights, b, 240)

        #Run when circadian switch is turned on
        self.listen_state(self.set_lights_quick, "input_boolean.circadian", new = "on")

        #Run when bathroom is turned on
        self.listen_state(self.set_toilet, "light.bathroom", new = "on", old = "off")

        #Run when monitor is turned on or circadian offset is changed
        self.listen_state(self.set_lights_quick, "light.monitor", new = "on", old = "off")

        #Run when offset is changed
        self.listen_state(self.set_lights_quick, "input_select.circadian_hour")
        self.listen_state(self.set_lights_quick, "input_select.circadian_minute")

        self.set_lights_quick()

    def set_lights(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on":
            self.setlight("light.monitor", 240, 1.4)
            self.setlight("light.reol", 240, 0.4)
            self.setlight("light.loft", 240, 0.6)
            #self.log("Updating lights, time is {}, color temp is {} and brightness is {}".format(self.now.time(), self.global_vars["c_colortemp"], self.global_vars["c_brightness"]))
        else:
            self.log("Circadian switch is off, lights not updated")

    def set_lights_quick(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on":
            self.log("Updating lights quickly,\n    Color: {}\n    Brightness: {}".format(self.global_vars["c_colortemp"], self.global_vars["c_brightness"]))
            self.setlight("light.monitor", 5, 1.4)
            self.setlight("light.reol", 2, 0.4)
            self.setlight("light.loft", 1, 0.6)
        else:
            # self.log("Circadian switch is off, lights not updated")
            pass

    def set_toilet(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on":
            self.setlight("light.bathroom", 1, 1.4)

    def setlight(self, light, transition, modifier):
        if self.get_state(light) == "on":
            self.turn_on(light, transition = transition, xy_color = self.global_vars["c_colortemp"], brightness = modifier * self.global_vars["c_brightness"])
