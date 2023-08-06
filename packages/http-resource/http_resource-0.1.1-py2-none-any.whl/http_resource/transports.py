import urllib

from dictutils import AttrDict
from .compat import imap, quote, urljoin
from .utils import encode_params, APIObject, new_api_object


class BaseTransport(object):

    def __init__(self, endpoint_url=None, timeout=None, proxy=None, user_agent=None, verify=True):
        self.endpoint_url = endpoint_url
        self.timeout = timeout
        self.proxy = proxy
        self.user_agent = user_agent or 'python-http-resource'
        self.verify = verify

    def __call__(self, session, method, *args, **kwargs):

        if not self.endpoint_url.endswith('/'):
            self.endpoint_url += '/'

        uri = urljoin(self.endpoint_url, '/'.join(imap(quote, args)))
        data = kwargs.get('data', None)

        if method == 'get':
            uri = '%s?%s' % (uri, urllib.parse.urlencode(data))
        else:
            if data and isinstance(data, dict):
                kwargs['data'] = encode_params(data)

        if self.verify:
            kwargs.setdefault('verify', self.verify)
        else:
            kwargs.setdefault('verify', False)

        response = self.get_response(session, method, uri, **kwargs)
        return self.handle_response(response)

    def get_endpoint_url(self, *parts):
        return urljoin(self._request.resource.endpoint_url, '/'.join(imap(quote, parts)))

    def get_headers(self, headers):
        return headers

    def get_response(self, session, method, uri, **kwargs):
        return getattr(session, method)(uri, **kwargs)

    def handle_response(self, response):
        return response


class RestTransport(BaseTransport):
    def get_headers(self, headers):
        headers.setdefault('Content-Type', 'application/json')
        return headers

    def results_iter(self, response, **kwargs):
        results = response.json()

        for result in results:
            yield AttrDict(result)

    def _make_api_object(self, response, model_type=None):
        data = response.json()
        # data = blob.get('data', None)
        # All valid responses have a "data" key.
        # if data is None:
        #     raise build_api_error(response, blob)
        # Warn the user about each warning that was returned.
        # warnings_data = blob.get('warnings', None)
        # for warning_blob in warnings_data or []:
        #     message = "%s (%s)" % (
        #         warning_blob.get('message', ''),
        #         warning_blob.get('url', ''))
        #     # warnings.warn(message, UserWarning)

        # pagination = blob.get('pagination', None)
        kwargs = {
            'response': response,
            # 'pagination': pagination and new_api_object(None, pagination, APIObject),
            # 'warnings': warnings_data and new_api_object(None, warnings_data, APIObject),
        }
        if isinstance(data, dict):
            obj = new_api_object(self, data, model_type, **kwargs)
        else:
            obj = APIObject(self, **kwargs)
            obj.data = new_api_object(self, data, model_type)
        return obj
