from importlib import import_module


api_version = 'v1'
urls = import_module('apollo.api.%s.urls' % api_version)