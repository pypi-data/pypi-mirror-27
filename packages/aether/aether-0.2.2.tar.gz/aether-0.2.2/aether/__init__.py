print("Welcome to Aether Platform.")
# Logger for within this __init__ file.
import logging

from aether.Sky import Sky as SkyEngine
# User mechanics
from aether.base.AppSupport import AppSupport
from aether.base.QueryParameter import QueryParameter
from aether.base.SessionConfig import SessionConfig
# Sky request/response Placeholder objects
from aether.base.placeholder.PlaceholderPolygon import PlaceholderPolygon
# User objects
from aether.dataobjects.AEPolygon import AEPolygon
from aether.dataobjects.Spacetime import Spacetime
from aether.proto.api_pb2 import PlaceholderSpacetimeBuilder
# Sky request/response objects
from aether.proto.api_pb2 import SpacetimeBuilder, HttpResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

######################################################################
#
# Registration sets the client UUID. Authentication occurs on the server
# side during each call.
#
######################################################################
def register(uuid):
    SessionConfig.getInstance().uuid = uuid

######################################################################
#
# Resources are data platforms (e.g., GeoTiff data layer) against which
# algorithms, analytics, and meta-algorithms can be run.
#
# For instance, the LandSat-8 Resource is a GeoTiff data layer, against
# which search (a metadata algorithm) or crop (a data algorithm) and so
# on can be run against.
#
# Each algorithm is executed by an aether client, which holds and separates
# the execution code of the developer from the request code of the user.
#
# The aether client is default to REST API interactions with the aether
# data platform, although, in principal, a user can create their own
# client to operate their own specific interactions with Resource objects.
#
# In a few special cases, such as search, the default GeoTiffResource has
# methods that specify functions to access the search using more "familiar"
# code syntax, e.g., Resource("landsat-8").search(), instead of more general
# code patterns like Resource("landsat-8").operate(client, method, parameters).
#
######################################################################
import aether.resources

def Resource(resource_name):
    _resources = {
        "landsat": resources.LandSat(),
        "sentinel": resources.Sentinel(),
        "cropland_data_layer": resources.CroplandDataLayer(),
    }

    if resource_name not in _resources:
        logger.error("Resource {} not found. Available resources: {}".format(resource_name, _resources.keys()))
        return None
    return _resources[resource_name]


######################################################################
#
# Sky() is the system of channels that inter-regulate or connect
# cloud-based elements with the end user, i.e., Sky() is how a user
# connects with the Cloud.
#
######################################################################

def Sky():
    return SkyEngine(SessionConfig.getInstance().aether_client())
