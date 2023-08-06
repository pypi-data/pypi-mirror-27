import dill
import base64
from google.protobuf import json_format

class sky_utils(object):

    @staticmethod
    def serialize_to_bytestring(o):
        b = bytearray()
        b.extend(dill.dumps(o, protocol=2))
        return str(b)

    @staticmethod
    def deserialize_from_bytestring(s):
        return dill.loads(bytes(s))

    @staticmethod
    def serialize_for_url(o):
        return base64.urlsafe_b64encode(str(o))

    @staticmethod
    def deserialize_from_url(s):
        return base64.urlsafe_b64decode(str(s))

    @staticmethod
    def serialize_numpy(n):
        return base64.b64encode(n)

    @staticmethod
    def deserialize_numpy(s):
        return base64.b64decode(s)

    @staticmethod
    def serialize_pb(pb):
        return json_format.MessageToJson(pb)

    @staticmethod
    def deserialize_pb(s, pb):
        return json_format.Parse(s, pb)