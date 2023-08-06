from aether.app_io_utilities import app_io_utilities
import json
import copy
import requests


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class aether_client(object):

    _rest_entrypoints = dict(
        SearchResource=dict(entry="/api/v1.0/search/{resource_name}/", method="POST"),
        ClipAndShipResource=dict(entry="/api/v1.0/sky/clip_and_ship/", method="POST"),

        UserAdminInterface=dict(entry="/api/v1.0/sky/user_admin/", method="POST"),
        DataModelData=dict(entry="/api/v1.0/datamodel/data/", method="POST"),

        AppSupportInterface=dict(entry="/api/v1.0/sky/app_support/", method="POST"),
        GatewaySpacetimeBuilder=dict(entry="/api/v1.0/sky/download/", method="POST"),
        SkyApplicationManifest=dict(entry="/api/v1.0/sky/application/", method="POST"),

        EndpointConsumerInterface=dict(entry="/api/v1.0/sky/{uuid}/application/{application_id}/", method="GET"),
    )

    def __init__(self, uuid, hostport=None):
        self._uuid = uuid
        self._hostport = hostport
        self._protocol = "http://"

    def _make_call(self, request, hostport):
        logger.info("Making REST call to: {} with {}".format(hostport, request))
        try:
            url = "{protocol}{hostport}{entry}".format(protocol=self._protocol, hostport=hostport, entry=request["entry"])
            headers = {'Content-Transfer-Encoding': 'base64'}
            response = requests.request(request["method"], url, json=request["data"], headers=headers)
        except Exception, err:
            raise RuntimeError("REST call Failed: {}".format(request))
        return response

    def _make_request(self, entry_name, entry_parameters, uri_parameters):
        if entry_name not in self._rest_entrypoints:
            raise ValueError("Requested entrypoint unrecognized: {}".format(entry_name))

        request = copy.deepcopy(self._rest_entrypoints[entry_name])
        try:
            request["entry"] = request["entry"].format(**entry_parameters)
        except Exception:
            raise ValueError("Requested entrypoint required parameters missing: {}".format(entry_name))

        request["data"] = uri_parameters
        return request

    def post_to(self, entry_name, entry_parameters, uri_parameters, output_structure=None, app=None):
        uri_parameters.update(dict(uuid=self._uuid))

        # if input_structure is not None:
        #     uri_parameters = self.serialize_to_input(uri_parameters, input_structure)
        #     if uri_parameters is None:
        #         logger.error("uri_parameters incorrectly formed by input_structure.")
        #         return None

        request = self._make_request(entry_name, entry_parameters, uri_parameters)

        if app is not None:
            return app.add(request, None, output_structure, "MICROSERVICE")
        return self.post_request(request, output_structure)

    def post_request(self, request, output_structure):
        response = self._make_call(request, self._hostport)
        if response is None:
            logger.error("Request failed.")
            return None

        if not response.ok:
            logger.error("Request failed: {}".format(response.reason))
            return None

        try:
            content = json.loads(response.content)
        except Exception:
            logger.error("Request returned ill formed JSON: {}".format(response.content))
            return None

        if output_structure is not None:
            return app_io_utilities.marshal_output(content, output_structure)
        return content
