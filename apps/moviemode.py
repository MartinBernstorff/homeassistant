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

class MovieMode(appapi.AppDaemon):

    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))
        #Setup the switch object
        switch = self.args["switch"]

        #Register callback for switch turning on
        self.listen_state(self.on, switch, new = "on")
        self.listen_state(self.off, switch, new = "off")

    def on(self, entity, attribute, old, new, kwargs):
        self.log("Moviemode on!")
        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily

        if self.get_state("media_player.pioneer") == "off":
            self.turn_on("media_player.pioneer")

            i = 0
            while (i < 10) and self.get_state("media_player.pioneer") == "off":
                time.sleep(2)
                i += 1
                self.log("Receiver is off, checking in 2 seconds, i = {}".format(i))
        elif self.get_state("media_player.pioneer") == "on":
            self.log("Receiver is already on, proceding")

        self.turn_on("script.moviemode")
        self.turn_on("switch.benq")
        self.setstate("light.monitor", 0, 10)
        self.setstate("light.loft", 0, 8)
        self.setstate("light.reol", 0, 13)

        self.turn_off("light.loft")
        self.turn_off("light.reol")
        self.turn_off("light.monitor")
        self.turn_off("light.hallway")
        self.turn_off("light.bathroom")

    def off(self, entity, attribute, old, new, kwargs):
        #Setup circadian dependencies

        self.now = datetime.datetime.now()
        self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
        self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)

        self.setstate("light.monitor", self.brightness, 40, self.hue)
        self.setstate("light.reol", self.brightness, 40, self.hue)
        self.setstate("light.loft", self.brightness, 40, self.hue)

        i = 0
        while (i<10):
            vollevel = int(self.get_state("media_player.pioneer", "volume_level")) - (0.03 * i)
            self.call_service("media_player/volume_set", entity_id = "media_player.pioneer", volume_level = vollevel)
            time.sleep(0.25)
            i += 1

        self.turn_off("switch.benq")
        self.turn_off("media_player.pioneer")
        self.turn_on("input_boolean.circadian") #Turn circadian adjustments back on
        self.log("Moviemode off!")

    def setstate(self, lt, bness, fade, color=""):
        self.modulator = 1
        switch = self.args["switch"]

        self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s")

        if color != "":
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade, xy_color = color)
        else:
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade)
