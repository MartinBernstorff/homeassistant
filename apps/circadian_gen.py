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
        self.now = self.datetime()
        b = self.now + datetime.timedelta(seconds=3)

        #Setup the input_selects
        self.update_time()
        self.listen_state(self.update_time, "input_select.circadian_hour")
        self.listen_state(self.update_time, "input_select.circadian_minute")

        self.listen_state(self.gen_circ_colortemp, "input_select.circadian_hour")
        self.listen_state(self.gen_circ_colortemp, "input_select.circadian_minute")

        self.listen_state(self.gen_circ_brightness, "input_select.circadian_hour")
        self.listen_state(self.gen_circ_brightness, "input_select.circadian_minute")

        #Setup run_every
        self.run_every(self.gen_circ_brightness, b, 4 * 60)
        self.run_every(self.gen_circ_colortemp, b, 4 * 60)

    def gen_circ_brightness(self, entity="", attribute="", old="", new="", kwargs=""):
        t0 = self.now.replace(hour=5, minute=0, second=0) + self.global_vars["c_offset"]
        t1 = self.now.replace(hour=6, minute=0, second=0) + self.global_vars["c_offset"]
        t2 = self.now.replace(hour=13, minute=0, second=0) + self.global_vars["c_offset"]
        t3 = self.now.replace(hour=19, minute=0, second=0) + self.global_vars["c_offset"]
        t4 = self.now.replace(hour=21, minute=0, second=0) + self.global_vars["c_offset"]
        t5 = self.now.replace(hour=21, minute=0, second=0) + self.global_vars["c_offset"]

        if self.now > t0 and self.now <= t1:
            self.set_circ_brightness(1.65, 0, t1, t0)
        elif self.now > t1 and self.now <= t2:
            self.set_circ_brightness(2.5, 1.65, t2, t1)
        elif self.now > t2 and self.now <= t3:
            self.global_vars["c_brightness"] = 638
        elif self.now > t3 and self.now <= t4:
            self.set_circ_brightness(1.0, 2.5, t4, t3)
        elif self.now > t4 and self.now <= t5:
            self.set_circ_brightness(0.08, 1.0, t5, t4)
        else:
            self.global_vars["c_brightness"] = 20

        #self.log("Set new circ brightness {} at {}".format(self.global_vars["c_brightness"], self.now))

    def set_circ_brightness(self, endbness, startbness, endtime, starttime):
        base = 255
        start = startbness
        end = endbness
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        self.global_vars["c_brightness"] = (start + (end - start) * position / fadelength) * base

    def gen_circ_colortemp(self, entity="", attribute="", old="", new="", kwargs=""):
        t0 = self.now.replace(hour=4, minute=0, second=0) + self.global_vars["c_offset"]
        t1 = self.now.replace(hour=5, minute=0, second=0) + self.global_vars["c_offset"]
        t2 = self.now.replace(hour=13, minute=0, second=0) + self.global_vars["c_offset"]
        t3 = self.now.replace(hour=19, minute=0, second=0) + self.global_vars["c_offset"]
        t4 = self.now.replace(hour=20, minute=0, second=0) + self.global_vars["c_offset"]
        t5 = self.now.replace(hour=21, minute=0, second=0) + self.global_vars["c_offset"]

        if self.now > t0 and self.now <= t1:
            self.set_circ_colortemp(0.4255, 0.5268, 0.3998, 0.4133, t1, t0)
        elif self.now > t1 and self.now <= t2:
            self.set_circ_colortemp(0.3136, 0.4255, 0.3237, 0.3998, t2, t1)
        elif self.now > t2 and self.now <= t3:
            self.set_circ_colortemp(0.4255, 0.3136, 0.3998, 0.3237, t3, t2)
        elif self.now > t3 and self.now <= t4:
            self.set_circ_colortemp(0.5268, 0.4255, 0.4133, 0.3998, t4, t3)
        elif self.now > t4 and self.now <= t5:
            self.set_circ_colortemp(0.704, 0.5268, 0.296, 0.4133, t5, t4)
        else:
            self.global_vars["c_colortemp"] = [ 0.704, 0.296 ]

        #self.log("Set new circ brightness {} at {}".format(self.global_vars["c_brightness"], self.time()))

    def set_circ_colortemp(self, end_x, start_x, end_y, start_y, endtime, starttime):
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        self.x_now = start_x + (end_x - start_x) * position / fadelength
        self.y_now = start_y + (end_y - start_y) * position / fadelength

        self.global_vars["c_colortemp"] = [ self.x_now, self.y_now]

    def update_time(self, entity="", attribute="", old="", new="", kwargs=""):
        self.hour = int(self.get_state("input_select.circadian_hour"))
        self.minute = int(self.get_state("input_select.circadian_minute"))
        self.global_vars["c_offset"] = datetime.timedelta(hours=self.hour, minutes=self.minute)
        self.log("Circadian_gen_updated time offset set to {}".format(self.global_vars["c_offset"]))

"""
[ 0.674, 0.322 ] #Red initial
[ 0.5268, 0.4133 ] #Warm orange
[ 0.4255, 0.3998 ] #Bright orange
"""
