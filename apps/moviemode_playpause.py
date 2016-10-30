import appdaemon.appapi as appapi
import circadian_gen
import time
import datetime

#
# Moviemode_playpause app
#

class MovieModePlayPause(appapi.AppDaemon):

    def initialize(self):
        self.log("Initializing {}".format(__name__))

        #Register callback for switch turning on

        self.listen_state(self.on, "media_player.rasplex", new="playing")
        self.listen_state(self.off, "media_player.rasplex", new="paused")
    def on(self, entity, attribute, old, new, kwargs):
        self.log("Playing! at ".format(time.time()))

        self.turn_off("light.monitor")
        self.turn_off("light.reol")
        self.turn_off("light.loft")
        self.turn_off("light.hallway")

    def off(self, entity, attribute, old, new, kwargs):
        self.log("Paused! at ".format(time.time()))

        #Setup circadian dependencies
        self.now = datetime.datetime.now()
        self.hue = circadian_gen.CircadianGen.get_circ_hue(self)
        self.brightness = circadian_gen.CircadianGen.get_circ_brightness(self)

        self.setstate("light.monitor", 100, 10, self.hue)
        time.sleep(5)
        self.setstate("light.reol", self.brightness * 0.2, 10, self.hue)

    def setstate(self, lt, bness, fade, color=""):
        self.modulator = 1

        self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s")

        if color != "":
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade, xy_color = color)
        else:
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade)
