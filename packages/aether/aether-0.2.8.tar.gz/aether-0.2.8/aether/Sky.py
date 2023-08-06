
"""The Sky object provides user-developers with an interface to the Aether Platform
and larger functionality of cloud applications. Nearly every action taken by Aether
user-developers is built or executed by a method on the Sky object either through
direct method call or using the Sky object to pass-through a cloud operation to 
the Aether Platform ecosystem of applications and users.

The Aether Client provides a wrapper to most of the REST microservice calls that form
the foundation of the Aether ecosystem. The typical inheritance motif of the Sky object
is to receive an operating client in its constructor, then to use standard methods on the
Sky object to manage call methods on the client.

The Sky object provides the interface to the general application operating system of the
Aether Platform. In addition to this, methods are provided to give more conventional access
to high use operations like searching, cropping, and downloading through familiar direct
access to these applications using the Sky object.

In addition to this, methods are provided on the Sky object to:

1) :py:class:`~services.UserAdminServices`: manage the user and user account,
2) :py:class:`~services.AppSupportServices`: publish and interact with published applications,

For more information on these services see their respective classes.
"""

from aether.proto import api_pb2
from aether.sky_utils import sky_utils
from aether.services.UserAdminServices import UserAdminServices
from aether.services.AppSupportServices import AppSupportServices
from aether.base.SessionConfig import SessionConfig

class Sky(UserAdminServices, AppSupportServices):

    def __init__(self, aether_client):
        self._aether_client = aether_client

    def search(self, resource_name, polygon, query_parameters, app=None):
        """Search a Resource for inclusion of a polygon matching query parameters.

        Args:
            resource_name (string): The name of the resource to search.

            polygon (:py:class:`~dataobjects.AEPolygon.AEPolygon`): The polygon, representing the lat-lng coordinates of the region of interest.

            query_parameters (dict): Key-value pairs of parameter name and value.
                See :py:class:`~base.QueryParameters.QueryParameters` for more information.

            app (:py:class:`~base.AppSupport.AppSupport`): Either an AppSupport object or None. Using
                AppSupport will compile the microservice into a deferred application
                for use; otherwise, passing None will execute the microservice
                at runtime.

        Returns:
            response (:py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`): a SpacetimeBuilder if successful, and None
             if not. Returns a PlaceholderSpacetimeBuilder if app is not None.

            The SpacetimeBuilder contains a set of instructions to run another
            as a request to another application.

            The PlaceholderSpacetimeBuilder is returned when app is an AppSupport
            object. Its methods are equivalent to SpacetimeBuilder (so that code that
            follows will compile), but does not include the results of having run the
            application. Instead, the PlaceholderSpacetimeBuilder contains instructions
            to be substituted at runtime by the SpacetimeBuilder of the actual
            microservice output.
        """
        query_parameters.update(dict(polygon=polygon.to_latlngs()))
        output_structure = api_pb2.SpacetimeBuilder()
        response = self._aether_client.post_to("SearchResource",
                                               dict(resource_name=resource_name),
                                               query_parameters,
                                               output_structure=output_structure,
                                               app=app)
        return response

    def crop(self, builder, app=None):
        """Apply the crop application to a time series of imagery and polygon represented as a SpacetimeBuilder.

        Args:
            builder (:py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`): The SpacetimeBuilder request contains a time series, each of which consists
             of a list of stubs which are concatenated as bands, then cropped to match the layout of the polygon.

            app (:py:class:`~base.AppSupport.AppSupport`): Either an AppSupport object or None. Using AppSupport will
             compile the microservice into a deferred application for use; otherwise, passing None will execute the
             microservice at runtime.

        Returns:
            response (:py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`) A SpacetimeBuilder if successful, and None
             if not. Returns a PlaceholderSpacetimeBuilder if app is not None.

        The :py:class:`~base.SpacetimeBuilder.SpacetimeBuilder` contains a time series of stubs, each of which is a
        cropped GeoTiff created by the application. A mask (.msk) file is generated, if applicable, and a color table
        is appended for each stub which also has a color table added.
        """
        output_structure = api_pb2.SpacetimeBuilder()
        uri_parameters = dict(builder=sky_utils.serialize_pb(builder))
        # input_structure = ["builder"]
        response = self._aether_client.post_to("ClipAndShipResource",
                                               {},
                                               uri_parameters,
                                               # input_structure=input_structure,
                                               output_structure=output_structure,
                                               app=app)

        return response

    def download(self, builder, run=None, app=None):
        """Downloads the contents of a :py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`, i.e., a time series of imagery masked to a polygon.

        Args:
            builder (:py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`): The SpacetimeBuilder request contains a time series, each of which consists
             of a list of stubs which are concatenated as bands, stacked into a time series, and downloaded.

            run (list): A list of any functions which accepts a Spacetime object (not protobuffer) as input
                and products a Spacetime object as output can be sent along with the SpacetimeBuilder to be run prior to
                download. This allows a convenient and lightweight mechanism for running simple algorithms in the cloud.
                The functions are limited to native python and numpy operations, if the method imports numpy.

            app (:py:class:`~base.AppSupport.AppSupport`): Either an AppSupport object or None. Using AppSupport will
                compile the microservice into a deferred application for use; otherwise, passing None will execute the
                microservice at runtime.

        Returns:
            response (Spacetime): a Spacetime protocol buffer if successful, and None if not. Returns a PlaceholderSpacetime if app
                is not None.

            The Spacetime contains a time series of imagery, each of which is a cropped and masked to the dimensions of
            the originating polygon. The metadata for the originating earliest timestamp GeoTiff is included as well.
        """
        if run is not None:
            byte_ops = [sky_utils.serialize_to_bytestring(r) for r in run]
            for op in byte_ops:
                bop = builder.btops.add()
                bop.serialized_func = op

        uri_parameters = dict(builder=sky_utils.serialize_pb(builder), method="DownloadSpacetime")
        output_structure = api_pb2.Spacetime()
        response = self._aether_client.post_to("GatewaySpacetimeBuilder",
                                               {},
                                               uri_parameters,
                                               # input_structure=input_structure,
                                               output_structure=output_structure,
                                               app=app)
        return response



    def RunApplicationWithPayload(self, payload, polygon):
        """Runs a compiled applications from using its payload string.

        Args:
            payload (str): The product of :py:class:`~Sky.Sky` :py:meth:`~dataobjects.AppSupportServices.AppSupportServices.ApplicationPayload` method.
            polygon (:py:class:`~dataobjects.AEPolygon.AEPolygon`): The polygon, representing the lat-lng coordinates of the region of interest.

        Returns:
            response (:py:class:`HttpResponse`): a dictionary containing the application results, usually a serialized
                string containing an image.
        """
        uri_parameters = dict(polygon=polygon.to_latlngs(),
                              payload=payload)

        response = self._aether_client.post_to("SkyApplicationManifest",
                                               {},
                                               uri_parameters)

        return response

    def RunApplicationWithId(self, application_id, polygon, as_uuid=None):
        """Runs a compiled applications from using its Application Id string.

        Args:
            application_id (str): The application id of the saved application after calling the
                :py:class:`~Sky.Sky` :py:meth:`~dataobjects.AppSupportServices.AppSupportServices.PublishApplication` method.
            polygon (:py:class:`~dataobjects.AEPolygon.AEPolygon`): The polygon, representing the lat-lng coordinates of the region of interest.

        Returns:
            response (:obj:`HttpResponse`): a dictionary containing the application results, usually a serialized
             string containing an image.
        """
        if as_uuid is None:
            as_uuid = SessionConfig.getInstance().uuid
        uri_parameters = dict(polygon=polygon.to_latlngs())
        response = self._aether_client.post_to("EndpointConsumerInterface",
                                               dict(uuid=as_uuid, application_id=application_id),
                                               uri_parameters)
        return response
