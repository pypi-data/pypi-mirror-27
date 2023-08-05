import os
from skywiserestclient import SkyWiseJSON, SkyWiseResource


class HistoricalObsResource(SkyWiseJSON, SkyWiseResource):

    @classmethod
    def set_app_id(self, app_id):
        HistoricalObsResource.set_user(app_id)

    @classmethod
    def set_app_key(self, app_key):
        HistoricalObsResource.set_password(app_key)
    pass

_site = os.getenv('SKYWISE_HISTORICAL_OBS_SITE', 'https://historical-obs.api.wdtinc.com')
_user = os.getenv('SKYWISE_HISTORICAL_OBS_APP_ID', '')
_password = os.getenv('SKYWISE_HISTORICAL_OBS_APP_KEY', '')

HistoricalObsResource.set_site(_site)
HistoricalObsResource.set_user(_user)
HistoricalObsResource.set_password(_password)

from .station import Station
