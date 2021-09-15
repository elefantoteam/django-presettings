from django.http import JsonResponse

def error_404(request, exception):
    data = {
        'message': 'Url not found',
        'error_type': 'not_found',
        'field': None
    }
    resp = {
        'error': True,
        'message' : 'Page not found',
        'data': data
    }
    response = JsonResponse(data=resp)
    response.status_code = 404
    return response

def error_500(request):
    data = {
        'message': 'An error occured, its on us',
        'error_type': 'internal',
        'field': None
    }
    resp = {
        'error': True,
        'message' : 'Inernal server error',
        'data': data
    }
    response = JsonResponse(data=resp)
    response.status_code = 404
    return response