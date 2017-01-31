import appdaemon.appapi as appapi
import time
import datetime
from rgb_xy import Converter

conv = Converter()

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   light: The light that's used for sunrise


class Sunrise(appapi.AppDaemon):
    def initialize(self):
        self.log("Initializing sunrise")
        self.switch = self.args["switch"] # The switch to turn on/off the sunrise
        self.entity = "light.monitor" # The light to act as sun
        self.update_time() # Get the current time-input
        # Callbacks
        self.listen_state(self.update_time, "input_select.sunrise_hour")
        self.listen_state(self.update_time, "input_select.sunrise_minute")
        self.listen_state(self.circadian_update_time, "input_select.circadian_hour")
        self.listen_state(self.circadian_update_time, "input_select.circadian_minute")

        # self.listen_state(self.rise2, self.args["switch"], new = "on") # Callback for testing
    def rise(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_off("input_boolean.circadian")
        self.natural()
        self.turn_on("input_boolean.circadian")

    def update_time(self, entity="", attribute="", old="", new="", kwargs=""):
        self.hour = self.get_state("input_select.sunrise_hour")
        self.minute = self.get_state("input_select.sunrise_minute")
        self.log("Time set to {}:{}".format(self.hour, self.minute))
        time = datetime.time(int(self.hour), int(self.minute), 0)
        self.cancel_timer(self.sunrise)
        self.sunrise = self.run_daily(self.rise, time)

    def circadian_update_time(self, entity="", attribute="", old="", new="", kwargs=""):
        """
        Called when circadian offset is modified.
        Sets new sunrise time.
        """
        self.log("Updating sunrise time")
        self.now = datetime.datetime.now()
        time.sleep(2) # Sleep for 2 seconds to make sure that c_offset has updated
        self.sunrise = self.now.replace(hour=7, minute=0, second=0) + self.global_vars["c_offset"]
        self.set_state("input_select.sunrise_hour", state = self.sunrise.hour)
        self.set_state("input_select.sunrise_minute", state = self.sunrise.minute)

    #######################
    # Different sequences #
    #######################

    def red_only(self, entity="", attribute="", old="", new="", kwargs=""):
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=1, t_fade=1, color=[0.674, 0.322])
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=10, t_fade=1800, color=[0.674, 0.322])
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=100, t_fade=1800, color=[0.5268, 0.4133])

    def natural(self, entity="", attribute="", old="", new="", kwargs=""):
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=1, t_fade=1, color=conv.rgb_to_xy(255, 0, 0))
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=1, t_fade=180, color=conv.rgb_to_xy(255, 255, 255))
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=255, t_fade=1800, color=conv.rgb_to_xy(255, 255, 255))

    def condseq_on(self, switch=None, entity=None, brightness=None, t_fade=0, color=None, post_delay=0):
        """
            A function for conditional sequentilization
            Takes the following arguments:

            switch: An input boolean that's conditional for the step to be executed
            entity: The entity to be affected

            For lights:
            brightness: End brightness [0-255]
            fade: How long the fade should take (in seconds)
            color: End colour [X, Y]
            post_delay: How long after the action there should be an additional delay (in seconds)
        """
        device, entity_id = self.split_entity(self.entity)
        if switch is not None:
            if self.get_state(switch) == "on":
                if device == "light":
                    if color is not None:
                        self.turn_on(entity, brightness = brightness, transition = t_fade, xy_color = color)
                        time.sleep(t_fade)
                        time.sleep(post_delay)
                    else:
                        self.turn_on(entity, brightness = brightness, transition = t_fade)
                        time.sleep(t_fade)
                        time.sleep(post_delay)
                self.turn_on(entity)
