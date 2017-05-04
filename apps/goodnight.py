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
        self.turn_off("group.all_lights")
        self.turn_off("media_player.pioneer")
        self.turn_off("input_boolean.mm")
        self.turn_off("input_boolean.circadian")
        self.turn_off("input_boolean.sunrise")
        self.turn_off("input_boolean.carpediem")
        self.turn_off("group.all_lights")
        self.turn_off(self.switch)
