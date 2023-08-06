########################################################################################
#
# A Singleton class for managing global values across modules, to be inherited.
#
########################################################################################

from aether.aether_client import aether_client

class SessionConfig():

    _local_hostport = "127.0.0.1:5002"
    _default_hostport = "data.runsonaether.com:5002"

    hostport = _default_hostport
    uuid = None

    def aether_client(self):
        return aether_client(self.uuid, hostport=self.hostport)

    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SessionConfig.__instance == None:
            SessionConfig()
        return SessionConfig.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SessionConfig.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SessionConfig.__instance = self

    def _switch_service_locality(self, to_local=False):
        if to_local:
            self.hostport = self._local_hostport
        else:
            self.hostport = self._default_hostport
