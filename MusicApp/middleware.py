# MusicApp/middleware.py
from django.shortcuts import redirect
import re


class CustomRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        match = re.match(r'^/name=(?P<name>[^&]*)&store=(?P<store>[^&]*)$', path)
        if match:
            name = match.group('name')
            store = match.group('store')
            query_params = f'?name={name}&store={store}'
            return redirect(f'/track/{query_params}')

        response = self.get_response(request)
        return response
