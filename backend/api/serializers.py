from rest_framework import serializers
from .models import Participant, Blacklist, Draw, DrawResult

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'email']

class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blacklist
        fields = ['id', 'participant', 'blocked_participant']

class DrawResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawResult
        fields = ['id', 'giver', 'receiver']

class DrawSerializer(serializers.ModelSerializer):
    results = DrawResultSerializer(many=True, read_only=True)

    class Meta:
        model = Draw
        fields = ['id', 'date', 'results']
