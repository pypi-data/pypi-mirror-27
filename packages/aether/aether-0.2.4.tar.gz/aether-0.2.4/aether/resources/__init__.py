from aether.base.GeoTiffResource import GeoTiffResource
from aether.base.QueryParameter import QueryParameter

class LandSat(GeoTiffResource):
    _resource_name = "landsat"

    _query_parameters = [
        QueryParameter("cloud_cover", QueryParameter.Type.FLOAT, False, QueryParameter.Collect.RANGE, [0.0, 1.0], "Excludes scenes with Cloud Fractions outside this range."),
        QueryParameter("date_acquired", QueryParameter.Type.TIMEDATE, False, QueryParameter.Collect.RANGE, ["1900-01-01", "2050-01-01"], "Excludes dates outside this range."),
        QueryParameter("bands", QueryParameter.Type.STRING, False, QueryParameter.Collect.MANY, ["B2", "B3", "B4"], "Band numbers returned in query."),
        QueryParameter("spacecraft_id", QueryParameter.Type.STRING, False, QueryParameter.Collect.MANY, ["LANDSAT_7", "LANDSAT_8"], "Spacecraft name: LANDSAT_4 through LANDSAT_8."),
        QueryParameter("collection_number", QueryParameter.Type.STRING, False, QueryParameter.Collect.ONE, "01", "Collection number: either 'PRE' or '01'."),
    ]

    def __init__(self):
        super(LandSat, self).__init__(self._resource_name, self._query_parameters)

class Sentinel(GeoTiffResource):
    _resource_name = "sentinel"

    _query_parameters = [
        QueryParameter("cloud_cover", QueryParameter.Type.FLOAT, False, QueryParameter.Collect.RANGE, [0.0, 1.0], "Excludes scenes with Cloud Fractions outside this range."),
        QueryParameter("date_acquired", QueryParameter.Type.TIMEDATE, False, QueryParameter.Collect.RANGE, ["1900-01-01", "2050-01-01"], "Excludes dates outside this range."),
        QueryParameter("bands", QueryParameter.Type.STRING, False, QueryParameter.Collect.MANY, ["B02", "B03", "B04"], "Band numbers returned in query, B01 through B12, or B8A."),
    ]

    def __init__(self):
        super(Sentinel, self).__init__(self._resource_name, self._query_parameters)

class CroplandDataLayer(GeoTiffResource):
    _resource_name = "cropland_data_layer"

    _query_parameters = [
        QueryParameter("year", QueryParameter.Type.TIMEDATE, True, QueryParameter.Collect.MANY, ["2016"], "Calendar Year of the Cropland Data Layer (published in January of the following year)."),
    ]

    def __init__(self):
        super(CroplandDataLayer, self).__init__(self._resource_name, self._query_parameters)