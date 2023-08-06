
##################################################################################################
#
# The GeoTiffResource breaks slightly from the Inversion of Control paradigm for constructing
# analytics and their relationships with resources. I.e., search is in theory a meta analytic
# that operates on the resource.
#
# Instead this Resource object provides common user-expected methods that link to whatever way
# the analytics are implemented. This simplifies the user experience and makes it familiar.
#
##################################################################################################
import aether as ae

class GeoTiffResource(object):

    def __init__(self, resource_name, query_parameters):
        self._resource_name = resource_name
        self._query_parameters = query_parameters

    def QueryParameters(self):
        return self._query_parameters

    def search(self, polygon, query_parameters, app=None):
        return ae.Sky().search(self._resource_name, polygon, query_parameters, app=app)
