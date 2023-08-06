import requests
import six

from dictutils import AttrDict
from .utils import import_module


class Empty(object):
    pass


class Request(object):
    def __init__(self, resource):
        self.resource = resource
        self.method = 'get'
        self.headers = {
            'User-Agent': 'http-resource/1.0',
            'Accept-Encoding': ', '.join(('gzip', 'deflate')),
            'Accept': '*/*',
            'Connection': 'keep-alive',
        }
        self.data = {}
        self.low_mark, self.high_mark = 0, None  # Used for offset/limit

    def clone(self, klass=None, **kwargs):
        obj = Empty()
        obj.__class__ = klass or self.__class__
        obj.resource = self.resource
        obj.method = self.method
        obj.headers = self.headers
        obj.data = self.data
        obj.low_mark, obj.high_mark = self.low_mark, self.high_mark

        return obj

    def set_method(self, method):
        self.method = method

    def set_data(self, *args, **kwargs):
        for kw in kwargs.items():
            if kw[1] is not None:
                self.data[kw[0]] = kw[1]

    def set_limits(self, low=None, high=None):
        """
        Adjusts the limits on the rows retrieved. We use low/high to set these,
        as it makes it more Pythonic to read and write. When the SQL query is
        created, they are converted to the appropriate offset and limit values.

        Any limits passed in here are applied relative to the existing
        constraints. So low is added to the current low value and both will be
        clamped to any existing high value.
        """
        if high is not None:
            if self.high_mark is not None:
                self.high_mark = min(self.high_mark, self.low_mark + high)
            else:
                self.high_mark = self.low_mark + high
        if low is not None:
            if self.high_mark is not None:
                self.low_mark = min(self.high_mark, self.low_mark + low)
            else:
                self.low_mark = self.low_mark + low

    def clear_limits(self):
        """
        Clears any existing limits.
        """
        self.low_mark, self.high_mark = 0, None


class HttpResource(object):
    name = None
    endpoint_url = None
    auth_class = None
    transport_class = None

    def __init__(self, *args, **kwargs):
        self._args = args
        self._result_cache = None
        self.request = kwargs.pop('request', None) or Request(self)

    def __getitem__(self, k):
        """
        Retrieves an item or slice from the set of results.
        """
        if not isinstance(k, (slice,) + six.integer_types):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0)) or
                (isinstance(k, slice) and (k.start is None or k.start >= 0) and
                 (k.stop is None or k.stop >= 0))), \
            "Negative indexing is not supported."

        if self._result_cache is not None:
            return self._result_cache[k]

        if isinstance(k, slice):
            qs = self._clone()
            if k.start is not None:
                start = int(k.start)
            else:
                start = None
            if k.stop is not None:
                stop = int(k.stop)
            else:
                stop = None
            qs.request.set_limits(start, stop)
            return list(qs)[::k.step] if k.step else qs

        qs = self._clone()
        qs.request.set_limits(k, k + 1)
        return list(qs)[0]

    def __iter__(self):
        if self._result_cache is None:
            self._result_cache = list(self._iterator())
        return iter(self._result_cache)

    def __str__(self):
        return iter(list(self._iterator()))

    def _clone(self, klass=None, **kwargs):
        if klass is None:
            klass = self.__class__

        request = self.request.clone()

        c = klass(*self._args, request=request)
        c.__dict__.update(kwargs)
        return c

    def _fetch(self, **kwargs):

        endpoint_url = self.get_endpoint_url()

        self.transport = self.get_transport(endpoint_url=endpoint_url)

        session = requests.session()
        session.auth = self.get_auth()
        session.headers.update(self.transport.get_headers(self.request.headers))

        kwargs.update({'data': self.get_request_data(self.request.data, **kwargs)})

        return self.transport(session, self.request.method, *self._args, **kwargs)

    def _iterator(self):
        results = self._fetch()

        for row in self.results_iter(results):
            yield row

    def get_auth(self, ):
        if self.auth_class:
            auth_class_str = self.settings.get('auth')
            auth_class = import_module(auth_class_str)

            return auth_class(**self.settings)

        return None

    def get_transport(self, **kwargs):
        if self.transport_class is None:
            from .transports import RestTransport
            self.transport_class = RestTransport
        else:
            if type(self.transport_class) is str:
                self.transport_class = import_module(self.transport_class)

        return self.transport_class(**kwargs)

    def get_endpoint_url(self):
        return self.endpoint_url

    def get_request_data(self, data, **kwargs):
        return data

    def data(self, *args, **kwargs):
        clone = self._clone()
        clone.request.data = {}
        clone.request.set_data(*args, **kwargs)
        return clone

    def first(self):
        """
        Returns the first object of a query, returns None if no match is found.
        """
        objects = list((self)[:1])
        if objects:
            return objects[0]
        return None

    def count(self):
        return None

    def get(self, *args, **params):
        self.request.set_method('get')
        return list(self._iterator())

    def post(self, *args, **params):
        self.request.set_method('post')
        return list(self._iterator())

    def results_iter(self, response, **kwargs):
        results = response.json()

        if type(results) is dict:
            if 'result' in results:
                results = results.get('result')

        for result in results:
            yield AttrDict(result)
