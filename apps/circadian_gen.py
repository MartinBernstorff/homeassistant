import appdaemon.appapi as appapi
import datetime
import time

#
# Circadian app
#
# Args:
#   None atm.

class CircadianGen(appapi.AppDaemon):

    def initialize(self):
        self.log("CircadianGen initialized")
        self.now = datetime.datetime.now()
        b = self.now + datetime.timedelta(0, 3)

        #Set time intervals
        self.now = datetime.datetime.now()


    def get_circ_brightness(self, l=""):
        t0 = self.now.replace(hour=5, minute=0, second=0)
        t1 = self.now.replace(hour=6, minute=30, second=0)
        t2 = self.now.replace(hour=13, minute=0, second=0)
        t3 = self.now.replace(hour=19, minute=30, second=0)
        t4 = self.now.replace(hour=21, minute=0, second=0)
        t5 = self.now.replace(hour=21, minute=20, second=0)

        if self.now > t0 and self.now <= t1:
            CircadianGen.set_circ_brightness(self, 1.65, 0, t1, t0)
        elif self.now > t1 and self.now <= t2:
            CircadianGen.set_circ_brightness(self, 2.5, 1.65, t2, t1)
        elif self.now > t2 and self.now <= t3:
            self.brightness = 638
        elif self.now > t3 and self.now <= t4:
            CircadianGen.set_circ_brightness(self, 1.0, 2.5, t4, t3)
        elif self.now > t4 and self.now <= t5:
            CircadianGen.set_circ_brightness(self, 0.05, 1.0, t5, t4)
        else:
            self.brightness = 3

        return self.brightness

        #self.log("Set new circ brightness {} at {}".format(self.brightness, self.now))

    def set_circ_brightness(self, endbness, startbness, endtime, starttime):
        base = 255
        start = startbness
        end = endbness
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        self.brightness = (start + (end - start) * position / fadelength) * base

    def get_circ_hue(self, l=""):
        t0 = self.now.replace(hour=5, minute=0, second=0)
        t1 = self.now.replace(hour=7, minute=0, second=0)
        t2 = self.now.replace(hour=13, minute=0, second=0)
        t3 = self.now.replace(hour=19, minute=0, second=0)
        t4 = self.now.replace(hour=20, minute=30, second=0)
        t5 = self.now.replace(hour=21, minute=20, second=0)

        if self.now > t0 and self.now <= t1:
            CircadianGen.set_circ_colortemp(self, 0.4255, 0.5268, 0.3998, 0.4133, t1, t0)
        elif self.now > t1 and self.now <= t2:
            CircadianGen.set_circ_colortemp(self, 0.3136, 0.4255, 0.3237, 0.3998, t2, t1)
        elif self.now > t2 and self.now <= t3:
            CircadianGen.set_circ_colortemp(self, 0.4255, 0.3136, 0.3998, 0.3237, t3, t2)
        elif self.now > t3 and self.now <= t4:
            CircadianGen.set_circ_colortemp(self, 0.5268, 0.4255, 0.4133, 0.3998, t4, t3)
        elif self.now > t4 and self.now <= t5:
            CircadianGen.set_circ_colortemp(self, 0.704, 0.5268, 0.296, 0.4133, t5, t4)
        else:
            self.colortemp = [ 0.704, 0.296 ]

        return self.colortemp

        #self.log("Set new circ brightness {} at {}".format(self.brightness, self.now))

    def set_circ_colortemp(self, end_x, start_x, end_y, start_y, endtime, starttime):
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        self.x_now = start_x + (end_x - start_x) * position / fadelength
        self.y_now = start_y + (end_y - start_y) * position / fadelength

        self.colortemp = [ self.x_now, self.y_now]

"""
[ 0.674, 0.322 ] #Red initial
[ 0.5268, 0.4133 ] #Warm orange
[ 0.4255, 0.3998 ] #Bright orange
"""
