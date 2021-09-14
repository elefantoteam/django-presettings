from rest_framework.routers import DefaultRouter
from .views import JustViewSet


router = DefaultRouter()
router.register(r'test', JustViewSet)

urlpatterns = [] + router.urls
