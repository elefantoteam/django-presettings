from rest_framework import serializers

class ErrorDetailSerializer(serializers.Serializer):
    ERROR_TYPES = (
        ('blank', 'blank'),
        ('required', 'required'),
        ('unique', 'unique'),
        ('null', 'null'),
        ('invalid', 'invalid'),
    )

    message = serializers.CharField()
    error_type = serializers.ChoiceField(choices=ERROR_TYPES)
    field = serializers.CharField()



class BadRequestSerializer(serializers.Serializer):
    error = serializers.BooleanField()
    message = serializers.CharField()
    data = ErrorDetailSerializer(many=True)