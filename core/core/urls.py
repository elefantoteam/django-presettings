from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# OPTIONAL
# import debug_toolbar


schema_view = get_schema_view(
    openapi.Info(
        title="PROJECT API",
        default_version='v1',
        description="You can see privacy policy here: /api/user/privacy/",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hello@elefanto.kz"),
        license=openapi.License(name="Johny License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/my-app/', include('my_app.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
        # path('__debug__/', include(debug_toolbar.urls)), # optional
    ]
