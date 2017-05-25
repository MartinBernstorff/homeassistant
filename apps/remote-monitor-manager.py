import appdaemon.appapi as appapi
import subprocess

class RemoteMonitorManager(appapi.AppDaemon):

    def initialize(self, entity="", attribute="", old="", new="", kwargs=""):
        "Initializing"

        self.log("Initializing remote-monitor-manager")

        self.path = "/home/martin/Work/remote-monitor-manager/script.sh"
        self.switch = "light.monitor"

        self.listen_state(self.run, self.switch, old="on", new="off")

    def run(self, entity="", attribute="", old="", new="", kwargs=""):
        "Function that'll run bash script"

        self.log("Running!")
        output = subprocess.check_output(self.path, shell=True)
