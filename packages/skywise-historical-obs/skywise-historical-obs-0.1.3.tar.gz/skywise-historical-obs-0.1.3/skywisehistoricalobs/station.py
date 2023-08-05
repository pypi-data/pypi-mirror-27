from voluptuous import Schema, Any
from skywiserestclient.validation import (datetime, datetime_to_str,
                                          latitude as latitude_type,
                                          longitude as longitude_type)
from skywisehistoricalobs import HistoricalObsResource
from skywisehistoricalobs.observation import StationObservation


class Station(HistoricalObsResource):

    _path = '/stations/{latitude}/{longitude}'

    _deserialize = Schema({
        'id': Any(unicode, None),
        'description': Any(unicode, None),
        'location': {
            'latitude': Any(latitude_type, None),
            'longitude': Any(longitude_type, None),
            'elevation': Any(float, None)
        },
        'earliest_recorded_at': Any(datetime, None),
        'latest_recorded_at': Any(datetime, None),
        'distance': Any(float, None)
    }, required=False)

    _serialize = Schema({
        'id': Any(unicode, None),
        'description': Any(unicode, None),
        'location': {
            'latitude': Any(latitude_type, None),
            'longitude': Any(longitude_type, None),
            'elevation': Any(float, None)
        },
        'earliest_recorded_at': Any(datetime_to_str, None),
        'latest_recorded_at': Any(datetime_to_str, None),
        'distance': Any(float, None)
    }, required=False)

    _args = Schema({
        'limit': Any(int, None),
        'radius': Any(float, int, None)
    }, required=False)

    def __init__(self, **kwargs):
        super(Station, self).__init__(**kwargs)

    def __repr__(self):
        return str(self.json())

    @classmethod
    def nearest(cls, latitude, longitude, **kwargs):
        return Station.find(latitude=latitude, longitude=longitude, **kwargs)

    def observations(self, **kwargs):
        return StationObservation.find(station_id=self.id, **kwargs)
