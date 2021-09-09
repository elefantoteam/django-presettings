from utils.error_serializers import BadRequestSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .serializers import JustModelSerializer
from .models import JustModel
from drf_yasg.utils import swagger_auto_schema


class JustViewSet(ModelViewSet):
    serializer_class = JustModelSerializer
    queryset = JustModel.objects.order_by()
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        responses={
            400: BadRequestSerializer,
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            400: BadRequestSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
