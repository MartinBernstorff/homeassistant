import appdaemon.appapi as appapi
import datetime
import time

#
# Circadian app
#
# Args:
#   None atm.

class Circadian(appapi.AppDaemon):

    def initialize(self):
        self.log("Circadian initialized")
        self.now = datetime.datetime.now()
        b = self.now + datetime.timedelta(0, 3)

    def get_circ_brightness(self, l=""):
        self.now = datetime.datetime.now()
        t0 = self.now.replace(hour=7, minute=0, second=0)
        t1 = self.now.replace(hour=8, minute=0, second=0)
        t2 = self.now.replace(hour=13, minute=0, second=0)
        t3 = self.now.replace(hour=18, minute=0, second=0)
        t4 = self.now.replace(hour=21, minute=0, second=0)
        t5 = self.now.replace(hour=21, minute=30, second=0)
        if self.now > t0 and self.now < t1:
            self.set_circ_brightness(0.5, 0, t1, t0)
        elif self.now > t1 and self.now < t2:
            self.set_circ_brightness(1, 0.5, t2, t1)
        elif self.now > t2 and self.now < t3:
            self.brightness = 255
        elif self.now > t3 and self.now < t4:
            self.set_circ_brightness(0.5, 1, t4, t3)
        elif self.now > t4 and self.now < t5:
            self.set_circ_brightness(0.5, 0, t5, t4)
        else:
            self.brightness = 0

        return self.brightness

        #self.log("Set new circ brightness {} at {}".format(self.brightness, self.now))

    def set_circ_brightness(self, endbness, startbness, endtime, starttime):
        base = 255
        start = startbness
        end = endbness
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        self.brightness = (start + (end - start) * position / fadelength) * base
