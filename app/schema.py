from apiflask import Schema
from marshmallow import fields, validate

MAX_PER_PAGE = 100


class PaginationSchema(Schema):
    page = fields.Int()
    per_page = fields.Int(validate=validate.Range(max=MAX_PER_PAGE))

class WeatherDataSchema(Schema):
    StationID = fields.Str()
    Year = fields.Int()
    Month = fields.Int()
    Date = fields.Int()
    MaxTemp = fields.Int()
    MinTemp = fields.Int()
    Precipitation = fields.Int()


class WeatherDataQuerySchema(PaginationSchema):
    StationID = fields.Str()
    Year = fields.Int()
    Month = fields.Int()
    Date = fields.Int()

class WeatherDataSummarySchema(Schema):
    StationID = fields.Str()
    Year = fields.Int()
    AvgMaxTemp = fields.Int()
    AvgMinTemp = fields.Int()
    TtlAccPrecipitation = fields.Int()


class WeatherDataSummaryQuerySchema(PaginationSchema):
    StationID = fields.Str()
    Year = fields.Int()
