import appdaemon.appapi as appapi

"""
 Off_scheduler

 Args:
   switch: entity_id of switch that starts script [input_boolean]
   devices: List of devices to be turned off [comma seperated list]
"""

class GoodNight(appapi.AppDaemon):

    def initialize(self, entity="", attribute="", old="", new="", kwargs=""):
        self.log("Initializing GoodNight")

        self.switch = self.args["switch"]
        self.listen_state(self.good_night, self.switch, old="off", new="on")

    def good_night(self, entity="", attribute="", old="", new="", kwargs=""):
        self.log("Starting good-night script")
        for device in self.split_device_list(self.args["devices"]):
            self.turn_off(device)
        self.turn_off(self.switch)
