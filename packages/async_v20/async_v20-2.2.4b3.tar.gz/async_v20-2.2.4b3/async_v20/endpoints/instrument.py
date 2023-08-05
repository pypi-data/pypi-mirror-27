from .annotations import *
from .base import EndPoint, Path
from ..definitions.primitives import *
from ..definitions.types import *

__all__ = ['GETInstrumentsCandles', 'GETInstrumentOrderBook', 'GETInstrumentsPositionBook']


class GETInstrumentsCandles(EndPoint):
    # the HTTP verb to use for this endpoint
    method = 'GET'

    # path to endpoint
    path = Path('/v3/instruments/', InstrumentName, '/candles')

    # description of endpoint
    description = 'Fetch candlestick data for an instrument.'

    # parameters required to send to endpoint
    parameters = [
        {'name': 'Authorization', 'located': 'header', 'type': Authorization, 'description': 'str'},
        {'name': 'Accept-Datetime-Format', 'located': 'header', 'type': AcceptDatetimeFormat,
         'description': 'AcceptDatetimeFormat'},
        {'name': 'instrument', 'located': 'path', 'type': InstrumentName, 'description': 'InstrumentName'},
        {'name': 'price', 'located': 'query', 'type': PriceComponent, 'description': 'str'},
        {'name': 'granularity', 'located': 'query', 'type': CandlestickGranularity,
         'description': 'CandlestickGranularity'},
        {'name': 'count', 'located': 'query', 'type': Count, 'description': 'int'},
        {'name': 'from', 'located': 'query', 'type': FromTime, 'description': 'DateTime'},
        {'name': 'to', 'located': 'query', 'type': ToTime, 'description': 'DateTime'},
        {'name': 'smooth', 'located': 'query', 'type': Smooth, 'description': 'boolean'},
        {'name': 'includeFirst', 'located': 'query', 'type': IncludeFirstQuery, 'description': 'boolean'},
        {'name': 'dailyAlignment', 'located': 'query', 'type': DailyAlignment, 'description': 'int'},
        {'name': 'alignmentTimezone', 'located': 'query', 'type': AlignmentTimezone, 'description': 'str'},
        {'name': 'weeklyAlignment', 'located': 'query', 'type': WeeklyAlignment,
         'description': 'WeeklyAlignment'},
    ]

    # valid responses
    responses = {
        200: {'instrument': InstrumentName, 'granularity': CandlestickGranularity, 'candles': ArrayCandlestick}}

    # error msgs'
    error = (400, 401, 404, 405)


class GETInstrumentOrderBook(EndPoint):
    # the HTTP verb to use for this endpoint
    method = 'GET'

    # path to endpoint
    path = Path('/v3/instruments/', InstrumentName, '/orderBook')

    # description of endpoint
    description = 'Fetch a gzip compressed order book for an instrument.'

    # parameters required to send to endpoint
    parameters = [
        {'name': 'Authorization', 'located': 'header', 'type': Authorization, 'description': 'str'},
        {'name': 'Accept-Datetime-Format', 'located': 'header', 'type': AcceptDatetimeFormat,
         'description': 'AcceptDatetimeFormat'},
        {'name': 'instrument', 'located': 'path', 'type': InstrumentName, 'description': 'InstrumentName'},
        {'name': 'time', 'located': 'query', 'type': DateTime, 'description': 'DateTime'},
    ]

    # valid responses
    responses = {200: {'orderBook': OrderBook}}

    # error msgs'
    error = (400, 401, 404, 405)


class GETInstrumentsPositionBook(EndPoint):
    # the HTTP verb to use for this endpoint
    method = 'GET'

    # path to endpoint
    path = Path('/v3/instruments/', InstrumentName, '/positionBook')

    # description of endpoint
    description = 'Fetch a gzip compressed position book for an instrument.'

    # parameters required to send to endpoint
    parameters = [
        {'name': 'Authorization', 'located': 'header', 'type': Authorization, 'description': 'str'},
        {'name': 'Accept-Datetime-Format', 'located': 'header', 'type': AcceptDatetimeFormat,
         'description': 'AcceptDatetimeFormat'},
        {'name': 'instrument', 'located': 'path', 'type': InstrumentName, 'description': 'InstrumentName'},
        {'name': 'time', 'located': 'query', 'type': DateTime, 'description': 'DateTime'},
    ]

    # valid responses
    responses = {200: {'positionBook': PositionBook}}

    # error msgs'
    error = (400, 401, 404, 405)
