from core.settings import env
# from rest_framework_json_api.pagination import JsonApiPageNumberPagination
# from rest_framework_json_api.metadata import JSONAPIMetadata
# from rest_framework.renderers import JSONRenderer
# from rest_framework.renderers import BrowsableAPIRenderer

DEBUG = env('DEBUG_ON') == '1'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.response_handler.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'utils.response_handler.CustomJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'utils.response_handler.CustomJsonApiPageNumberPagination',
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'PAGE_SIZE': 1000,
    'DATETIME_FORMAT': '%s',
    'DATE_FORMAT': '%s',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT')
    }
}