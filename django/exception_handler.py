"""
Add in settings.py:

MIDDLEWARE = [
  ...
  'ExceptionsHandler',
 ]

"""

__all__ = ["ExceptionsHandler", "HandledError"]

from django import template
from django.http import HttpResponseBadRequest
from django.shortcuts import render


class HandledError(Exception):
    pass


class ExceptionsHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if type(exception) is HandledError:
            try:
                template.loader.get_template("errorhandler.html")  # type: ignore
                return render(request, "errorhandler.html", {"error": exception})
            except template.TemplateDoesNotExist:
                return HttpResponseBadRequest(repr(exception))
