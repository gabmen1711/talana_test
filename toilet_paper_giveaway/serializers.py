from rest_framework import serializers
from .models import Participants, Winners


class PartcipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['name', 'last_name', 'email']
