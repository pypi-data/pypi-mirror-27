from aether.proto import api_pb2
from aether.sky_utils import sky_utils
from aether.base.SessionConfig import SessionConfig

class AppSupportServices(object):

    def ApplicationPayload(self, app, application_name="", description=""):
        sky_app = api_pb2.SkyApplication()
        sky_app.application_name = application_name
        sky_app.description = description
        sky_app.owner_uuid = SessionConfig.getInstance().uuid

        if len(app._messages) == 0:
            return sky_app

        sky_app.messages.extend(app._messages)
        # sky_app.input_structure = app._messages[0].input_structure
        sky_app.output_structure = app._messages[-1].output_structure
        return sky_utils.serialize_for_url(sky_utils.serialize_pb(sky_app))

    def PublishApplication(self, payload):
        uri_parameters = dict(payload=payload, method="PublishApp")
        response = self._aether_client.post_to("AppSupportInterface", {}, uri_parameters)
        return response

    def UpdateApplication(self, application_id, payload):
        uri_parameters = dict(payload=payload, method="UpdateApp", application_id=application_id)
        response = self._aether_client.post_to("AppSupportInterface", {}, uri_parameters)
        return response
