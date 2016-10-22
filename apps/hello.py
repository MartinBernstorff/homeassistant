import appdaemon.appapi as appapi

#
# Hellow World App
#
# Args:
#

class HelloWorld(appapi.AppDaemon):

  def initialize(self):
     self.log("You are now ready to run Apps!")
