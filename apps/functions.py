import time

def condseq_on(switch=None, entity=None, brightness=None, t_fade=0, color=None, post_delay=0):
    """
        A function for conditional sequentilization
        Takes the following arguments:

        switch: An input boolean that's conditional for the step to be executed
        entity: The entity to be affected

        If the entity is a light:
        brightness: End brightness [0-255]
        fade: How long the fade should take (in seconds)
        color: End colour [X, Y]
        post_delay: How long after the action there should be an additional delay (in seconds)
    """
    device, entity = self.split_entity(self.entity)
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
