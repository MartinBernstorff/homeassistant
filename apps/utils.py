import appdaemon.appapi as appapi
import time

class utils(appapi.AppDaemon):

    def initialize(self):
        """Initialization"""
        pass

    def cond_seq_set_state( self,
                            entity=None,
                            switch=None,
                            state=None,
                            brightness=None,
                            t_fade=0,
                            color=None,
                            post_delay=0,
                            modifier=1):
        """
            A function for conditional sequentilization

            Required arguments:
            state: End-state
            entity: The entity_id to be affected
            switch: An input boolean that's conditional for the sequence to
                keep running


            Optional arguments:
            post_delay: How long after the action there should be an
                additional delay (in seconds)
            modifier: Relative modifier for the delay
                lights:
                    brightness: End brightness [0-255]
                    fade: How long the fade should take (in seconds)
                    color: End colour [X, Y]

        """
        device, entity_id = self.split_entity(entity)
        if switch is not None and state is not None:
            if self.get_state(switch) == "on":
                if device == "light":
                    if state == "on":
                        if color is not None:
                            self.turn_on(entity, brightness=brightness, transition=t_fade * modifier, xy_color=color)
                            time.sleep(t_fade * modifier)
                            time.sleep(post_delay * modifier)
                        else:
                            self.turn_on(entity, brightness=brightness, transition=t_fade * modifier)
                            time.sleep(t_fade * modifier)
                            time.sleep(post_delay * modifier)
                    if state == "off":
                        self.turn_off(entity)
                if state == "on":
                    self.turn_on(entity)
                    time.sleep(post_delay * modifier)
                if state == "off":
                    self.turn_off(entity)
                    time.sleep(post_delay * modifier)
        else:
            self.log("Switch is {} and state is {}, exiting".format(switch, state), level="ERROR")
