from enum import Enum

class QueryParameter():

    class Collect(Enum):
        ONE = 1,
        RANGE = 2,
        MANY = 3,

    class Type(Enum):
        INT = 1,
        FLOAT = 2,
        STRING = 3,
        TIMEDATE = 4,

    class Ordered(object):
        FIRST = "QueryParameter.ORDERED.FIRST",
        LAST = "QueryParameter.ORDERED.LAST"

    _type_map = {
        Type.INT: int,
        Type.FLOAT: float,
        Type.STRING: str,
        Type.TIMEDATE: str,
    }

    _bigquery_query_type_map = {
        Type.INT: "INTEGER",
        Type.FLOAT: "FLOAT",
        Type.STRING: "STRING",
        Type.TIMEDATE: "STRING",
    }

    def __init__(self, name, type, is_required, collection, default_value, description):
        self.name = name
        self.type = type
        self.is_required = is_required
        self.collection = collection
        self.default_value = default_value
        self.description = description

    def add_reqparse_arg(self, parser, location):
        action = None
        if self.collection == self.Collect.MANY or self.collection == self.Collect.RANGE:
            action = "append"

        parser.add_argument(
            name=self.name,
            type=self._type_map[self.type],
            required=self.is_required,
            default=self.default_value,
            action=action,
            location=location
        )

    def bigquery_query_type_map(self, type):
        return self._bigquery_query_type_map[type]

    def render_for_sql(self, value):
        v = value
        if self.type == self.Type.STRING or self.type == self.Type.TIMEDATE:
            v = "'{}'".format(value)
        return v

    def is_ordered(self, value):
        if self.collection == self.Collect.RANGE and len(value) == 1:
            if value[0]==QueryParameter.Ordered.FIRST or value[0]==QueryParameter.Ordered.LAST:
                return True
        return False

    def ordered_condition(self, value, serverside_type_maps):
        n = self.name
        if n in serverside_type_maps:
            n = serverside_type_maps[n].format(n)
        if value[0] == QueryParameter.Ordered.FIRST:
            return "{} ASC".format(n)
        if value[0] == QueryParameter.Ordered.LAST:
            return "{} DESC".format(n)

    def where_conditions(self, value, serverside_type_maps):
        n = self.name
        if n in serverside_type_maps:
            n = serverside_type_maps[n].format(n)

        s = None
        if self.collection == self.Collect.ONE:
            s = "({n} = {v})".format(n=n, v=self.render_for_sql(value))
        elif self.collection == self.Collect.RANGE:
            s = "({n} >= {v0} AND {n} <= {v1})".format(n=n, v0=self.render_for_sql(value[0]), v1=self.render_for_sql(value[1]))
        elif self.collection == self.Collect.MANY:
            s = "(" + " OR ".join(["({0} = {1})".format(n, self.render_for_sql(v)) for v in value]) + ")"
        return s

    def __str__(self):
        return "{name:20s} {required:5s} {type:10s} {range:5s} Default {default:35s}: {description}".format(
            name=self.name,
            required="REQ" if self.is_required else "",
            type=self.type.name,
            range=self.collection.name,
            default=str(self.default_value),
            description=self.description)