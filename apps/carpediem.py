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
        self.listen_state(self.updatefactor, self.args["factor"])

        #Register callback for switch turning on
        self.listen_state(self.carpecorner, switch, new = "on")
        self.listen_state(self.carpereol, switch, new = "on")
        self.listen_state(self.carpebathroom, switch, new = "on")

        #Reset the switch at 20:00 each day
        time = datetime.time(20, 0, 0)
        self.run_daily(self.reset, time)

    def carpecorner(self, entity, attribute, old, new, kwargs):
        #Make short corner light var
        #Setup circadian dependencies
        self.now = datetime.datetime.now()
        self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
        self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)
        cl = "light.monitor"
        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        self.setstate(cl, 150, 60, [ 0.674, 0.322 ]) #Red initial
        self.setstate(cl, circadian_gen.CircadianGen.get_circ_brightness(self), 600, circadian_gen.CircadianGen.get_circ_hue(self)) #Circadian hue
        self.turn_on("input_boolean.circadian") #Turn back on circadian

    def carpebathroom(self, entity, attribute, old, new, kwargs):
        #Setup circadian dependencies
        self.now = datetime.datetime.now()
        self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
        self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)
        #Make short bathroom light var
        bl = "light.bathroom"
        self.setstate(bl, 150, 60, [ 0.674, 0.322 ])
        self.setstate(bl, circadian_gen.CircadianGen.get_circ_brightness(self), 600, circadian_gen.CircadianGen.get_circ_hue(self)) #Circadian hue


    def carpereol(self, entity, attribute, old, new, kwargs):
        #Setup circadian dependencies
        self.now = datetime.datetime.now()
        self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
        self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)
        #Make short reol light var
        rl = "light.reol"

        time.sleep(self.modulator * 300)
        self.setstate(rl, circadian_gen.CircadianGen.get_circ_brightness(self), 300, circadian_gen.CircadianGen.get_circ_hue(self)) #Circadian hue


    def setstate(self, lt, bness, fade, color=""):
        switch = self.args["switch"]

        if self.get_state(switch) == "on":
            self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s")

            if color != "":
                self.turn_on(lt, brightness = bness, transition = self.modulator * fade, xy_color = color)
            else:
                self.turn_on(lt, brightness = bness, transition = self.modulator * fade)


            time.sleep(self.modulator * fade)
        else:
            self.log("Switch turned off, terminating")

    # pylint: disable=too-many-arguments
    def updatefactor(self, entity="", attribute="", old="", new="", kwargs=""):
        self.factor_state = self.get_state(self.args["factor"])

        if self.factor_state == "1%":
            self.modulator = 0.01
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
