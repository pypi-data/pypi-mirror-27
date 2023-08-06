# coding: utf-8
import importlib
import json

import logging
import six


def import_module(val, raise_exception=True):
    """
    Attempt to import a class from a string representation.
    copied from: djang_rest_framework
            (https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/settings.py#L169)

    modified to raise exception by default

    Args:
        raise_exception: boolean to declare if method should return None or raise exception
        val: string representation of a class to import
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s'. %s: %s." % (val, e.__class__.__name__, e)
        logging.warning(ImportError(msg))
        if raise_exception:
            raise ImportError(msg)
    return None


def clean_params(params, drop_nones=True, recursive=True):
    """Clean up a dict of API parameters to be sent to the Coinbase API.
    Some endpoints require boolean options to be represented as integers. By
    default, will remove all keys whose value is None, so that they will not be
    sent to the API endpoint at all.
    """
    cleaned = {}
    for key, value in six.iteritems(params):
        if drop_nones and value is None:
            continue
        if recursive and isinstance(value, dict):
            value = clean_params(value, drop_nones, recursive)
        cleaned[key] = value
    return cleaned


def encode_params(params, **kwargs):
    """Clean and JSON-encode a dict of parameters."""
    cleaned = clean_params(params, **kwargs)
    return json.dumps(cleaned)


def new_api_object(client, obj, cls=None, **kwargs):
    if isinstance(obj, dict):
        if not cls:
            resource = obj.get('resource', None)
            cls = _resource_to_model.get(resource, None)
        if not cls:
            obj_keys = set(six.iterkeys(obj))
            for keys, model in six.iteritems(_obj_keys_to_model):
                if keys <= obj_keys:
                    cls = model
                    break
        cls = cls or APIObject
        result = cls(client, **kwargs)
        for k, v in six.iteritems(obj):
            result[k] = new_api_object(client, v)
        return result
    if isinstance(obj, list):
        return [new_api_object(client, v, cls) for v in obj]
    return obj


class APIObject(dict):
    """Generic class used to represent a JSON response from the Coinbase API.
    If you're a consumer of the API, you shouldn't be using this class directly.
    This exists to make it easier to consume our API by allowing dot-notation
    access to the responses, as well as automatically parsing the responses into
    the appropriate Python models.
    """
    __api_client = None
    __response = None
    __pagination = None
    __warnings = None

    def __init__(self, api_client, response=None, pagination=None, warnings=None):
        self.__api_client = api_client
        self.__response = response
        self.__pagination = pagination
        self.__warnings = warnings

    @property
    def api_client(self):
        return self.__api_client

    @property
    def response(self):
        return self.__response

    @property
    def warnings(self):
        return self.__warnings

    @property
    def pagination(self):
        return self.__pagination

    def refresh(self, **params):
        url = getattr(self, 'resource_path', None)
        if not url:
            raise ValueError("Unable to refresh: missing 'resource_path' attribute.")
        response = self.api_client._get(url, data=params)
        data = self.api_client._make_api_object(response, type(self))
        self.update(data)
        return data

    # The following three method definitions allow dot-notation access to member
    # objects for convenience.
    def __getattr__(self, *args, **kwargs):
        try:
            return dict.__getitem__(self, *args, **kwargs)
        except KeyError as key_error:
            attribute_error = AttributeError(*key_error.args)
            attribute_error.message = key_error.message
            raise attribute_error

    def __delattr__(self, *args, **kwargs):
        try:
            return dict.__delitem__(self, *args, **kwargs)
        except KeyError as key_error:
            attribute_error = AttributeError(*key_error.args)
            attribute_error.message = key_error.message
            raise attribute_error

    def __setattr__(self, key, value):
        # All attributes that start with '_' will not be accessible via item-getter
        # syntax, which means that they won't be included in conversion to a
        # vanilla dict, which means that APIObjects can be treated as equivalent to
        # dicts. This is nice because it allows direct JSON-serialization of any
        # APIObject.
        if key.startswith('_') or key in self.__dict__:
            return dict.__setattr__(self, key, value)
        return dict.__setitem__(self, key, value)

    # When an API response includes multiple items, allow direct accessing that
    # data instead of forcing additional attribute access. This works for
    # slicing and index reference only.
    def __getitem__(self, key):
        data = getattr(self, 'data', None)
        if isinstance(data, list) and isinstance(key, (int, slice)):
            return data[key]
        return dict.__getitem__(self, key)

    def __dir__(self):  # pragma: no cover
        # This makes tab completion work in interactive shells like IPython for all
        # attributes, items, and methods.
        return list(self.keys())

    def __str__(self):
        try:
            return json.dumps(self, sort_keys=True, indent=2)
        except TypeError:
            return '(invalid JSON)'

    def __name__(self):
        return '<{0} @ {1}>'.format(type(self).__name__, hex(id(self)))  # pragma: no cover

    def __repr__(self):
        return '{0} {1}'.format(self.__name__(), str(self))  # pragma: no cover


class Money(APIObject):
    def __str__(self):
        currency_str = '%s %s' % (self.currency, self.amount)
        # Some API responses return mappings that look like Money objects (with
        # 'amount' and 'currency' keys) but with additional information. In those
        # cases, the string representation also includes a full dump of the keys of
        # the object.
        if set(dir(self)) > set(('amount', 'currency')):
            return '{0} {1}'.format(
                currency_str, json.dumps(self, sort_keys=True, indent=2))
        return currency_str


_resource_to_model = {

}

_obj_keys_to_model = {
    frozenset(('amount', 'currency')): Money,
}
