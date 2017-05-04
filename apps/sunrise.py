import appdaemon.appapi as appapi
import time
import datetime
from rgb_xy import Converter

conv = Converter()

"""
Sunrise app

Args:
switch: The switch that initializes the script
light: The light that's used for sunrise


"""


class Sunrise(appapi.AppDaemon):
    def initialize(self):
        self.utils = self.get_app("utils")
        self.log("Initializing sunrise")
        self.switch = self.args["switch"] # The switch to turn on/off the sunrise

        self.entity = "light.bathroom" # The light to act as sun

        self.listen_state(self.rise, self.args["switch"], new="on") # Callback for testing

    def rise(self, entity="", attribute="", old="", new="", kwargs=""):
        """Function to start sunrise. Has the following internal variables:
            self.delay: How long after boolean turning on should the function run?
            self.modifier: Relative modifier of delays and fades
        """
        self.delay = 40
        self.modifier = 1

        self.turn_off("input_boolean.circadian")
        self.log("The sun is rising in {} mins!".format(self.delay))
        self.sunrise_timer = self.run_in(self.natural, self.delay * 60)


    #######################
    # Different sequences #
    #######################

    def natural(self, *args, **kwargs):
        self.log("Natural sunrise is running with switch {switch}, light {light} and modifier {modifier}".format(switch=self.switch, light=self.entity, modifier=self.modifier))
        self.utils.cond_seq_set_state(state="on", switch=self.switch, entity="light.monitor", brightness=1, t_fade=1, color=conv.rgb_to_xy(255, 255, 255), modifier=self.modifier)
        self.utils.cond_seq_set_state(state="on", switch=self.switch, entity="light.monitor", brightness=1, t_fade=500, color=conv.rgb_to_xy(255, 255, 255), modifier=self.modifier)
        self.utils.cond_seq_set_state(state="on", switch=self.switch, entity="light.monitor", brightness=15, t_fade=400, color=conv.rgb_to_xy(255, 255, 255), modifier=self.modifier)
        self.utils.cond_seq_set_state(state="on", switch=self.switch, entity=self.entity, brightness=1, t_fade=1, color=conv.rgb_to_xy(255, 255, 255), modifier=self.modifier)
        self.utils.cond_seq_set_state(state="on", switch=self.switch, entity=self.entity, brightness=1, t_fade=899, color=conv.rgb_to_xy(255, 255, 255), modifier=self.modifier)
        self.utils.cond_seq_set_state(state="on", switch=self.switch, entity=self.entity, brightness=255, t_fade=900, color=conv.rgb_to_xy(255, 255, 255), modifier=self.modifier)
        self.utils.cond_seq_set_state(state="on", switch=self.switch, entity="input_boolean.circadian")
