import appdaemon.appapi as appapi
import datetime
import time
from rgb_xy import Converter

conv = Converter()

#
# Circadian app
#
# Args:
#   None

class C_Gen_V2(appapi.AppDaemon):

    def initialize(self):
        self.log("C_Gen_V2 initialized")
        self.now = self.datetime()
        b = self.now + datetime.timedelta(seconds=1)

        #Setup the input_selects
        self.update_offset()
        self.listen_state(self.update_offset, "input_select.circadian_hour")
        self.listen_state(self.update_offset, "input_select.circadian_minute")

        self.listen_state(self.gen_c_brightness, "input_select.circadian_hour")
        self.listen_state(self.gen_c_brightness, "input_select.circadian_minute")

        self.listen_state(self.gen_c_color, "input_select.circadian_hour")
        self.listen_state(self.gen_c_color, "input_select.circadian_minute")

        #Setup run_every
        self.run_every(self.gen_c_brightness, b, 60)
        self.run_every(self.gen_c_color, b, 60)

        #Timepoints for brightness
        self.brightness_timepoint = [["00:00", 20],
                                     ["05:00", 20],
                                     ["06:00", 688],
                                     ["13:00", 688],
                                     ["19:00", 638],
                                     ["21:00", 128],
                                     ["21:15", 20],
                                     ["23:59", 20]
                                    ]

        #Timepoints for color
        self.color_timepoint = [["00:00", 255, 219, 147],
                                ["13:00", 244, 249, 255],
                                ["19:00", 255, 255, 255],
                                ["20:45", 255, 178, 67],
                                ["21:00", 255, 70, 0],
                                ["23:59", 255, 70, 0]
                               ]

    def gen_c_brightness(self, *args, **kwargs):
        i = 0
        for timepoint in self.brightness_timepoint:
            if i < len(self.brightness_timepoint) - 1: # Don't run the loop for 23:59

                t0 = self.now.replace(hour=int(self.brightness_timepoint[i][0][0:2]),
                                      minute=int(self.brightness_timepoint[i][0][3:5]),
                                      second=0) + self.global_vars["c_offset"]

                t1 = self.now.replace(hour=int(self.brightness_timepoint[i+1][0][0:2]),
                                      minute=int(self.brightness_timepoint[i+1][0][3:5]),
                                      second=0) + self.global_vars["c_offset"]

                if 1 == 0:
                    self.log("For run {} \n   t0: {}\n   t1: {}".format(i+1, t0, t1))

                if t0 < self.datetime() <= t1:
                    if 1 == 0:
                        self.log("\nTime is between \n    {} and \n    {}".format(t0, t1))

                    start = self.brightness_timepoint[i][1]
                    end = self.brightness_timepoint[i+1][1]
                    fade_length = (t1-t0).seconds
                    position = (self.now-t0).seconds

                    if 1 == 0:
                        self.log("c_brightness: {}".format((start + (end - start) * position / fade_length)))
                        self.log("\nstart: {}\nend: {}\nfade_length: {}\nposition: {}\n".format(
                            start, end, fade_length, position
                        ))

                    self.global_vars["c_brightness"] = (start + (end - start) * position / fade_length)
                i += 1

    def gen_c_color(self, *args, **kwargs):
        i = 0
        for timepoint in self.color_timepoint:
            if i < len(self.color_timepoint) - 1: # Don't run the loop for 23:59

                # TODO: Convert timepoint[i][0] and timepoint[i+1][0] to datetime objects
                t0 = self.now.replace(hour=int(self.color_timepoint[i][0][0:2]),
                                      minute=int(self.color_timepoint[i][0][3:5]),
                                      second=0) + self.global_vars["c_offset"]

                t1 = self.now.replace(hour=int(self.color_timepoint[i+1][0][0:2]),
                                      minute=int(self.color_timepoint[i+1][0][3:5]),
                                      second=0) + self.global_vars["c_offset"]

                if 1 == 0:
                    self.log("For run {} \n   t0: {}\n   t1: {}".format(i+1, t0, t1))

                if t0 < self.datetime() <= t1:
                    if 1 == 0:
                        self.log("\nTime is between \n    {}:{} and \n    {}:{}".format(self.color_timepoint[i][0][0:2],
                                                                                        self.color_timepoint[i][0][3:5],
                                                                                        self.color_timepoint[i+1][0][0:2],
                                                                                        self.color_timepoint[i+1][0][3:5]))

                    fade_length = (t1-t0).seconds
                    position = (self.now-t0).seconds

                    self.r_t0 = self.color_timepoint[i][1]
                    self.g_t0 = self.color_timepoint[i][2]
                    self.b_t0 = self.color_timepoint[i][3]

                    self.t0_xy = conv.rgb_to_xy(self.r_t0,
                                                self.g_t0,
                                                self.b_t0)

                    self.r_t1 = self.color_timepoint[i+1][1]
                    self.g_t1 = self.color_timepoint[i+1][2]
                    self.b_t1 = self.color_timepoint[i+1][3]

                    self.t1_xy = conv.rgb_to_xy(self.r_t1,
                                                self.g_t1,
                                                self.b_t1)

                    self.now_x = (self.t0_xy[0] + (self.t1_xy[0] - self.t0_xy[0]) * position / fade_length)
                    self.now_y = (self.t0_xy[1] + (self.t1_xy[1] - self.t0_xy[1]) * position / fade_length)

                    if 1 == 0:
                        self.log("c_colortemp: {}".format(self.global_vars["c_colortemp"]))

                    self.global_vars["c_colortemp"] = "[{}, {}]".format(self.now_x, self.now_y)
                i += 1

    def update_offset(self, entity="", attribute="", old="", new="", kwargs=""):
        self.hour = int(self.get_state("input_select.circadian_hour"))
        self.minute = int(self.get_state("input_select.circadian_minute"))
        self.global_vars["c_offset"] = datetime.timedelta(hours=self.hour, minutes=self.minute)
        self.log("c_offset: {}".format(self.global_vars["c_offset"]))
