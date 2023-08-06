import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserAdminServices(object):

    def UpgradeUserToDeveloper(self):
        parameters = dict(method="UpgradeUserToDeveloper")
        response = self._aether_client.post_to("UserAdminInterface", {}, parameters)
        return response

    def GetUserInformation(self):
        parameters = dict(method="GetUserInformation")
        response = self._aether_client.post_to("UserAdminInterface", {}, parameters)
        return response

