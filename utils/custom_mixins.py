import hashlib
import json

from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response


class RestCacheMixin(object):

    def __make_cache_key(self, **kwargs):
        return "%s_%s" % (
            self.__class__.__name__, hashlib.sha1(json.dumps(kwargs, sort_keys=True).encode('utf-8')).hexdigest())

    def dispatch(self, request, *args, **kwargs):
        cache_check = cache_key = None
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            self.initial(request, *args, **kwargs)

            cache_check = True if self.action == 'list' or (
                    request.user.is_anonymous and self.action == 'retrieve') else False

            if cache_check:
                cache_key = self.__make_cache_key(args=args, kwargs=kwargs, query_params=dict(request.query_params))
                cache_data = cache.get(cache_key)
                if cache_data:
                    return self.finalize_response(request, Response(data=cache_data), *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)

        if cache_check and self.response.status_code == 200:
            cache.set(cache_key, self.response.data, settings.CACHE_TIME)

        return self.response
