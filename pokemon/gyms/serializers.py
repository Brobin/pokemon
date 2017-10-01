from rest_framework.serializers import ModelSerializer

from .models import GymLog


class GymLogSerializer(ModelSerializer):

    class Meta:
        model = GymLog
        fields = ('created_at', 'mystic', 'valor', 'instinct')