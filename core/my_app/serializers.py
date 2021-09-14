from rest_framework import serializers
from .models import JustModel

class JustModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = JustModel
        fields = '__all__'
