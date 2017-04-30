import appdaemon.appapi as appapi
import circadian_gen
import time
import datetime

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

class CarpeDiem(appapi.AppDaemon):

    def initialize(self):
        self.log("Initializing carpe diem with switch: " + self.args["switch"])
        #Setup the switch object
        switch = self.args["switch"]

        #Update factor
        self.updatefactor()
        self.update_time()
        self.listen_state(self.updatefactor, self.args["factor"])

        #Register callback for switch turning on
        self.listen_state(self.carpe_monitor, switch, new = "on")
        self.listen_state(self.carpe_reol, switch, new = "on")
        self.listen_state(self.carpe_bathroom, switch, new = "on")
        self.listen_state(self.carpe_loft, switch, new = "on")

        #Reset the switch at 20:00 each day
        time = datetime.time(20, 0, 0)
        self.run_daily(self.reset, time)

    def carpe_monitor(self, entity, attribute, old, new, kwargs):
        #Make short corner light var
        #Setup circadian dependencies
        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        self.turn_off("input_boolean.sunrise") #Turn off sunrise if it's still on
        if self.get_state("light.monitor", "brightness") is None:
            self.setstate("light.monitor", brightness=1, fade=1, color=[ 0.674, 0.322 ]) #Red initial
            self.setstate("light.monitor", brightness=60, fade=60, color=self.global_vars["c_colortemp"])
            self.setstate("light.monitor", self.global_vars["c_brightness"], 600, color=self.global_vars["c_colortemp"]) #Circadian hue
        elif self.get_state("light.monitor", "brightness") < 60:
            self.setstate("light.monitor", brightness=60, fade=15, color=self.global_vars["c_colortemp"])
            self.setstate("light.monitor", self.global_vars["c_brightness"], 600, color=self.global_vars["c_colortemp"]) #Circadian hue
        elif self.get_state("light.monitor", "brightness") >= 60:
            self.setstate("light.monitor", self.global_vars["c_brightness"], 150, color=self.global_vars["c_colortemp"]) #Circadian hue
        self.turn_on("input_boolean.circadian") #Turn back on circadian
        self.turn_off(self.args["switch"])

    def carpe_bathroom(self, entity, attribute, old, new, kwargs):
        #Setup circadian dependencies
        #Make short bathroom light var
        bl = "light.bathroom"
        if self.get_state("light.bathroom", "brightness") is None:
            self.setstate(bl, brightness=1, fade=1, color=self.global_vars["c_colortemp"]) #Red initial
            self.setstate(bl, 150, 60, self.global_vars["c_colortemp"])
            self.setstate(bl, self.global_vars["c_brightness"], 600, self.global_vars["c_colortemp"]) #Circadian hue
        elif self.get_state("light.monitor", "brightness") <= 0:
            self.setstate(bl, self.global_vars["c_brightness"], 600, self.global_vars["c_colortemp"]) #Circadian hue
        elif self.get_state("light.monitor", "brightness") > 0:
            self.setstate(bl, 150, 60, self.global_vars["c_colortemp"])
            self.setstate(bl, self.global_vars["c_brightness"], 600, self.global_vars["c_colortemp"]) #Circadian hue

    def carpe_reol(self, entity, attribute, old, new, kwargs):
        #Make short reol light var
        rl = "light.reol"
        if self.get_state("light.monitor", "brightness") is None:
            time.sleep(self.modulator * 400)
            self.setstate(rl, self.global_vars["c_brightness"], 600, self.global_vars["c_colortemp"]) #Circadian hue
        elif self.get_state("light.monitor", "brightness") < 60:
            time.sleep(self.modulator * 400)
            self.setstate(rl, self.global_vars["c_brightness"], 600, self.global_vars["c_colortemp"]) #Circadian hue
        elif self.get_state("light.monitor", "brightness") >= 60:
            time.sleep(self.modulator * 30)
            self.setstate(rl, self.global_vars["c_brightness"], 600, self.global_vars["c_colortemp"]) #Circadian hue

    def carpe_loft(self, entity, attribute, old, new, kwargs):
        #Make short reol light var
        ll = "light.loft"
        if self.get_state("light.monitor", "brightness") is None:
            time.sleep(self.modulator * 600)
            self.setstate(ll, self.global_vars["c_brightness"], 300, self.global_vars["c_colortemp"]) #Circadian hue
        elif self.get_state("light.monitor", "brightness") < 60:
            time.sleep(self.modulator * 600)
            self.setstate(ll, self.global_vars["c_brightness"], 300, self.global_vars["c_colortemp"]) #Circadian hue
        elif self.get_state("light.monitor", "brightness") >= 60:
            time.sleep(self.modulator * 60)
            self.setstate(ll, self.global_vars["c_brightness"], 300, self.global_vars["c_colortemp"]) #Circadian hue

    def setstate(self, lt, brightness, fade, color=""):
        switch = self.args["switch"]

        if self.get_state(switch) == "on":
            self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s")

            if color != "":
                self.turn_on(lt, brightness = brightness, transition = self.modulator * fade, xy_color = color)
            else:
                self.turn_on(lt, brightness = brightness, transition = self.modulator * fade)

            time.sleep(self.modulator * fade)
        else:
            self.log("Switch turned off, terminating")

    # pylint: disable=too-many-arguments
    def updatefactor(self, entity="", attribute="", old="", new="", kwargs=""):
        self.factor_state = self.get_state(self.args["factor"])

        if self.factor_state == "1%":
            self.modulator = 0.01
        if self.factor_state == "10%":
            self.modulator = 0.1
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

    def update_time(self, entity="", attribute="", old="", new="", kwargs=""):
        self.hour = int(self.get_state("input_select.circadian_hour"))
        self.minute = int(self.get_state("input_select.circadian_minute"))
        self.log("Circadian time offset set to {}:{}".format(self.hour, self.minute))
