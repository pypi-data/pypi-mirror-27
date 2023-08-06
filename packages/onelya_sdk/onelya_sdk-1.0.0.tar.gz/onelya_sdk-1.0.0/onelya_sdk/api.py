from onelya_sdk.railway.reservation import Reservation as RailwayReservation
from onelya_sdk.references import References as References
from .railway.info import Info as RailwayInfo
from .railway.search import Search as RailwaySearch
from .session import Session
from .utils import get_array, get_item
from .wrapper import AgentAccount, RailwayPricingResponse
from .wrapper.requests import RequestWrapper

__version__ = 0.1

BALANCES_METHOD = 'Partner/V1/Info/Balances'
PRICING_METHOD = 'Insurance/V1/Search/Pricing'


class API(object):
    def __init__(self, username: str, password: str, pos: str):
        self.__session = Session(username, password, pos)
        self.__request_wrapper = RequestWrapper(self.__session)
        self.railway_search = RailwaySearch(self.__request_wrapper)
        self.railway_reservation = RailwayReservation(self.__request_wrapper)
        self.railway_info = RailwayInfo(self.__request_wrapper)
        self.references = References(self.__request_wrapper)

    def partner_balances(self):
        response = self.__request_wrapper.make_request(BALANCES_METHOD)
        return Balances(response)

    def railway_search_pricing(self):
        response = self.__request_wrapper.make_request(PRICING_METHOD, json={
            'Product': {
                '$type': 'ApiContracts.Insurance.V1.Products.Travel.Pricing.RailwayPricingRequest, ApiContracts'
            }
        })
        return Pricing(response)

    @property
    def last_response(self):
        return self.__session.last_response_data
    
    @property
    def last_request(self):
        return self.__session.last_request_data


class Balances(object):
    def __init__(self, json_data):
        self.account_balances = get_array(json_data.get('AccountBalances', None), AgentAccount)

        self.json_data = json_data


class Pricing(object):
    def __init__(self, json_data):
        self.pricing_response = get_item(json_data.get('PricingResponse', None), RailwayPricingResponse)

        self.json_data = json_data
