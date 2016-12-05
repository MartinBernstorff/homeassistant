import appdaemon.appapi as appapi

#
# Switch-linker
#
# Args:
#   master: The switch that's input
#   slave: The switch that follows along

class switch_linker(appapi.AppDaemon):

    def initialize(self):
        master = self.args["master"]
        slave = self.args["slave"]

        self.log("Initializing switch_linker with master: {} and slave: {}".format(master, slave))
        self.listen_state(self.on, master, new = "on")
        self.listen_state(self.off, master, new = "off")


    def on(self, entity="", attribute="", old="", new="", kwargs=""):
        self.toggle(self.args["slave"])

    def off(self, entity="", attribute="", old="", new="", kwargs=""):
        self.toggle(self.args["slave"])
