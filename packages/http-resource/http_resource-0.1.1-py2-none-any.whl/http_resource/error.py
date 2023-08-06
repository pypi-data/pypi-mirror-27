# coding: utf-8


class APIError(Exception):
    """Raised for errors related to interacting with the API server."""

    def __init__(self, response, id, message, errors=None):
        self.status_code = response.status_code
        self.response = response
        self.id = id or ''
        self.message = message or ''
        self.request = getattr(response, 'request', None)
        self.errors = errors or []

    def __str__(self):  # pragma: no cover
        return 'APIError(id=%s): %s' % (self.id, self.message)


class ParamRequiredError(APIError): pass


class ValidationError(APIError): pass


class InvalidRequestError(APIError): pass


class AuthenticationError(APIError): pass


class NotFoundError(APIError): pass


class InternalServerError(APIError): pass


class ServiceUnavailableError(APIError): pass





_error_id_to_class = {
    'param_required': ParamRequiredError,
    'validation_error': ValidationError,
    'invalid_request': InvalidRequestError,
    'authentication_error': AuthenticationError,
    'not_found': NotFoundError,
    'internal_server_error': InternalServerError,
}

_status_code_to_class = {
    400: InvalidRequestError,
    401: AuthenticationError,
    404: NotFoundError,
    422: ValidationError,
    500: InternalServerError,
    503: ServiceUnavailableError,
}
