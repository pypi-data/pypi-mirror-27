from voluptuous import Schema, Optional, Any
from skywiserestclient.validation import datetime, datetime_to_str
from skywisehistoricalobs import HistoricalObsResource


def _parameter_list_to_str(l):
    return ",".join(l)


_deserialize_obs = Schema({
    "id": Any(unicode, None),
    "recorded_at": Any(datetime, None),
    "measurements": [Schema({
        "parameter": Any(unicode, None),
        "value": Any(float, int, None),
        "unit": Any(unicode, None)
    })],
    Optional("metar"): Any(unicode, None),
    Optional("weather"): Any(unicode, None)
}, required=False)


_serialize_obs = Schema({
    "id": Any(unicode, None),
    "recorded_at": Any(datetime_to_str, None),
    "measurements": [Schema({
        "parameter": Any(unicode, None),
        "value": Any(float, int, None),
        "unit": Any(unicode, None)
    })],
    Optional("metar"): Any(unicode, None),
    Optional("weather"): Any(unicode, None)
}, required=False)


class StationObservation(HistoricalObsResource):

    _path = '/stations/{station_id}/observations'

    _deserialize = _deserialize_obs

    _serialize = _serialize_obs

    _args = Schema({
        "start": Any(datetime_to_str, None),
        "end": Any(datetime_to_str, None),
        "parameters": Any(_parameter_list_to_str, None)
    })

    def __repr__(self):
        return str(self.json())
