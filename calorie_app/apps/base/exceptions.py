from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class BadRequest(APIException):
    """
    Our validation error
    """
    status_code = status.HTTP_400_BAD_REQUEST


class CustomException(APIException):
    status_code = status.HTTP_428_PRECONDITION_REQUIRED

    def __init__(self, detail=None, code=None, error_code=None, meta=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        detail = {
            'detail': detail
        }

        if error_code:
            detail['error_code'] = error_code

        if meta:
            detail['meta'] = meta

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)
