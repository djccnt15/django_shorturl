import itertools

from django.contrib.gis.geoip2 import GeoIP2
from django.core.handlers.wsgi import WSGIRequest


def location_finder(request: WSGIRequest):
    return GeoIP2().country(query=request)


def dict_slice(d: dict, n: int):
    return dict(itertools.islice(d.items(), n))


def dict_filter(d: dict, filter_list: list):
    filtered = {}
    for k, v in d.items():
        if k in filter_list:
            filtered[k] = v
    return filtered
