from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json
from utils.static_variables import ERROR_CODES
from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from rest_framework.utils.urls import remove_query_param, replace_query_param
from collections import OrderedDict
from rest_framework.views import Response
from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS
)


class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type, renderer_context):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return b''

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS
        resp_data = data
        if "error" not in data:
            resp_data = {
                "error": False,
                "message": "Success",
                "data": data
            }

        ret = json.dumps(
            resp_data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )

        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: http://timelessrepo.com/json-isnt-a-javascript-subset
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()


class CustomJsonApiPageNumberPagination(JsonApiPageNumberPagination):
    """
    A json-api compatible pagination format.
    """
    page_query_param = 'page[number]'
    page_size_query_param = 'page[size]'
    max_page_size = 100

    def build_link(self, index):
        if not index:
            return None
        url = self.request and self.request.build_absolute_uri() or ''
        return replace_query_param(url, self.page_query_param, index)

    def get_paginated_response(self, data):
        resp_data = {
            'items': data,
            'pagination': OrderedDict([
                ('currentPage', self.page.number),
                ('totalPages', self.page.paginator.num_pages),
                ('totalCount', self.page.paginator.count),
                ('hasPrevious', self.page.has_next()),
                ('hasNext', self.page.has_previous()),
                ('pageSize', self.get_page_size(self.request))
            ])
        }

        return Response({
            'error': False,
            'message': 'Success',
            'data': resp_data
        })


def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError': _generic_error_handler,
        'Http404': _generic_error_handler,
        'PermissionDenied': _generic_error_handler,
        'NotAuthenticated': _authentication_error_handler
    }

    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _generic_error_handler(exc, context, response):
    error_messages = []
    print(exc, response.status_code == 404)
    if response.status_code == 404:
        error_messages.append({
            'message': 'Object not found',
            'error_type': 'not_found',
            'field': None
        })
    elif response.status_code == 400:
        for key, value in exc.detail.items():
            err = value[0]
            error_messages.append({
                'message': err,
                'error_type': err.code,
                'field': key
            })
    elif response.status_code == 403:
        error_messages.append({
            'message': 'Permission Denied',
            'error_type': 'no_permission',
            'field': None
        })
    response.data = {
        'error': True,
        'message': 'Validation Failed',
        'data': error_messages
    }
    return response


def _authentication_error_handler(exc, context, response):
    response.data = {
        'error': True,
        'message': 'Authentication Failed',
        'data': {
            'message': 'Please login to proceed',
            'error_type': 'no_auth',
            'field': None
        }
    }
    return response
