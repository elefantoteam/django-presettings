from utils.static_variables import ERROR_CODES
from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError': _validation_error_handler
    }

    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response

def _validation_error_handler(exc, context, response):
    error_messages = []
    for key, value in exc.detail.items():
        err = value[0]
        error_messages.append({
            'message': err,
            'error_type': err.code,
            'field': key
        })
    response.data = {
        "error": True,
        "message" : "Validation Failed",
        "data": error_messages

    }
    return response