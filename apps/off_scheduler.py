import appdaemon.appapi as appapi
import time
import datetime

"""
 Off_scheduler

 Args:
   switch: The switch that's required for the script to run
   entity: The entity to be controlled
"""

class OffScheduler(appapi.AppDaemon):

    def initialize(self, entity="", attribute="", old="", new="", kwargs=""):

        self.switch = self.args["switch"]
        self.hour = self.args["hour"]
        self.minute = self.args["minute"]
        self.entity = self.args["entity"]

        self.init = self.datetime().replace(hour=int(self.hour), minute=int(self.minute), second=0)
        offset = self.global_vars["c_offset"]
        run_at = (self.init + offset).time()

        self.log("Initializing OffScheduler with params: \n          switch: {}\n          run_at: {}\n          entity: {}".format(self.switch, run_at, self.entity))


        self.handle = self.run_daily(self.off, run_at)

        self.listen_state(self.update_time, "input_select.circadian_hour")
        self.listen_state(self.update_time, "input_select.circadian_minute")


    def off(self, entity="", attribute="", old="", new="", kwargs=""):
        device, entity = self.split_entity(self.entity)

        if self.args["switch"] is not None:
            if self.get_state(self.args["switch"]):
                if device == "light":
                    self.light_off()
                else:
                    self.turn_off(self.entity)
        else:
            if device == "light":
                self.light_off()
            else:
                self.turn_off(self.entity)

    def light_off(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state(self.entity) == "on":
            self.turn_on(self.entity, transition = 30, xy_color = self.global_vars["c_colortemp"], brightness = 0)
            time.sleep(30)
            self.turn_off(self.entity)
        else:
            self.turn_off(self.entity)

    def update_time(self, entity="", attribute="", old="", new="", kwargs=""):
        self.cancel_timer(self.handle)

        offset = self.global_vars["c_offset"]
        run_at = (self.init + offset).time()

        self.handle = self.run_daily(self.off, run_at)
        self.log("Initializing OffScheduler with params: \n          switch: {}\n          run_at: {}\n          entity: {}".format(self.switch, run_at, self.entity))
