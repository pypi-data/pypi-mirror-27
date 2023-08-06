from aether.app_io_utilities import app_io_utilities
import aether.aetheruserconfig as cfg
from aether_shared.utilities.user_api_utils import user_api_utils
import json
import copy
import requests
from session.Exceptions import SkyRuntimeError
import StringIO

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class aether_client(object):

    def __init__(self, uuid, hostport, protocol):
        self._uuid = uuid
        self._hostport = hostport
        self._protocol = protocol

    def _make_call(self, request, hostport):
        logger.info("Making REST call to: {} with {}".format(hostport, request))
        try:
            url = "{protocol}{hostport}{entry}".format(protocol=self._protocol, hostport=hostport, entry=request["entry"])
            headers = {'Content-Transfer-Encoding': 'base64'}
            response = requests.request(request["method"], url, json=request["data"], headers=headers, stream=True)

            if not response.ok:
                raise SkyRuntimeError("Request failed {}".format(response.reason))

            content = StringIO.StringIO()
            text_status = user_api_utils.rc_updating_format_text("Downloaded {mb:.{digits}f} MB...")
            bytes_transferred = 0
            for chunk in response.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    content.write(chunk)
                    bytes_transferred += len(chunk)
                    text_status.to_print(args=dict(mb=bytes_transferred / 1024. / 1024, digits=6))
            text_status.to_print(args=dict(mb=bytes_transferred / 1024. / 1024, digits=6), finished=True)

        except Exception, err:
            raise SkyRuntimeError(err)

        #
        # output = StringIO.StringIO()
        # output.write('First line.\n')
        # print >>output, 'Second line.'
        # bytes_transferred += len(chunk)
        # print("Downloaded {0} bytes".format(bytes_transferred))
        #
        # # Retrieve file contents -- this will be
        # # 'First line.\nSecond line.\n'
        # contents = output.getvalue()
        #
        # # Close object and discard memory buffer --
        # # .getvalue() will now raise an exception.
        # output.close()

        return response, content.getvalue()

    def _make_request(self, entry_name, entry_parameters, uri_parameters):
        if entry_name not in cfg._rest_entrypoints:
            raise SkyRuntimeError("Requested entrypoint unrecognized: {}".format(entry_name))

        request = copy.deepcopy(cfg._rest_entrypoints[entry_name])
        try:
            request["entry"] = request["entry"].format(**entry_parameters)
        except Exception:
            raise SkyRuntimeError("Requested entrypoint required parameters missing: {}".format(entry_name))

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
        response, r_content = self._make_call(request, self._hostport)

        if not response.ok:
            raise SkyRuntimeError("Request failed {}: {}".format(response.reason, r_content))

        try:
            content = json.loads(r_content)
        except Exception:
            raise SkyRuntimeError("Request returned ill formed JSON: {}".format(r_content))

        if output_structure is not None:
            return app_io_utilities.marshal_output(content, output_structure)
        return content
