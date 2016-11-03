import appdaemon.appapi as appapi
import datetime
import time
import shelve

#
# Circadian app
#
# Args:
#   None atm.

class CircadianGenUpdated(appapi.AppDaemon):
    def initialize(self):
        self.log("CircadianGenUpdated initialized")


        #Opens database file
        self.device_db = shelve.open("/etc/appdaemon/circadian.db")

        self.now = datetime.datetime.now()

        self.get_circ_brightness()
        self.get_circ_hue()

        #Setup callbacks
        b = self.now + datetime.timedelta(0, 3)
        self.run_every(self.get_circ_brightness, b, 120)
        self.run_every(self.get_circ_hue, b, 120)


    def get_circ_brightness(self, l=""):
        self.now = datetime.datetime.now()
        t0 = self.now.replace(hour=5, minute=30, second=0)
        t1 = self.now.replace(hour=9, minute=0, second=0)
        t2 = self.now.replace(hour=13, minute=0, second=0)
        t3 = self.now.replace(hour=19, minute=0, second=0)
        t4 = self.now.replace(hour=21, minute=0, second=0)
        t5 = self.now.replace(hour=22, minute=30, second=0)

        if self.now > t0 and self.now <= t1:
            CircadianGenUpdated.set_circ_brightness(self, 1.3, 0, t1, t0)
        elif self.now > t1 and self.now <= t2:
            CircadianGenUpdated.set_circ_brightness(self, 2.5, 1.3, t2, t1)
        elif self.now > t2 and self.now <= t3:
            self.brightness = 640
        elif self.now > t3 and self.now <= t4:
            CircadianGenUpdated.set_circ_brightness(self, 1.0, 2.5, t4, t3)
        elif self.now > t4 and self.now <= t5:
            CircadianGenUpdated.set_circ_brightness(self, 0.05, 1.0, t5, t4)
        else:
            self.brightness = 3

        #Saves to database under key "brightness"
        self.device_db["brightness"] = self.brightness

        #self.log("Set new circ brightness {} at {}".format(self.brightness, self.now))

    def set_circ_brightness(self, endbness, startbness, endtime, starttime):
        base = 255
        start = startbness
        end = endbness
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        self.brightness = (start + (end - start) * position / fadelength) * base

    def get_circ_hue(self, l=""):
        self.now = datetime.datetime.now()
        t0 = self.now.replace(hour=5, minute=30, second=0)
        t1 = self.now.replace(hour=9, minute=0, second=0)
        t2 = self.now.replace(hour=13, minute=0, second=0)
        t3 = self.now.replace(hour=19, minute=0, second=0)
        t4 = self.now.replace(hour=21, minute=0, second=0)
        t5 = self.now.replace(hour=22, minute=30, second=0)

        if self.now > t0 and self.now <= t1:
            CircadianGenUpdated.set_circ_colortemp(self, 0.4255, 0.5268, 0.3998, 0.4133, t1, t0)
        elif self.now > t1 and self.now <= t2:
            CircadianGenUpdated.set_circ_colortemp(self, 0.3136, 0.4255, 0.3237, 0.3998, t2, t1)
        elif self.now > t2 and self.now <= t3:
            CircadianGenUpdated.set_circ_colortemp(self, 0.4255, 0.3136, 0.3998, 0.3237, t3, t2)
        elif self.now > t3 and self.now <= t4:
            CircadianGenUpdated.set_circ_colortemp(self, 0.5268, 0.4255, 0.4133, 0.3998, t4, t3)
        elif self.now > t4 and self.now <= t5:
            CircadianGenUpdated.set_circ_colortemp(self, 0.674, 0.5268, 0.322, 0.4133, t5, t4)
        else:
            self.colortemp = [ 0.674, 0.322 ]

        self.device_db["hue"] = self.colortemp

        #self.log("Set new circ brightness {} at {}".format(self.brightness, self.now))

    def set_circ_colortemp(self, end_x, start_x, end_y, start_y, endtime, starttime):
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        self.x_now = start_x + (end_x - start_x) * position / fadelength
        self.y_now = start_y + (end_y - start_y) * position / fadelength

        self.colortemp = [ self.x_now, self.y_now]
        colortemp = [ self.x_now, self.y_now]

"""
[ 0.674, 0.322 ] #Red initial
[ 0.5268, 0.4133 ] #Warm orange
[ 0.4255, 0.3998 ] #Bright orange
"""
