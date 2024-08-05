from rest_framework import serializers
from .models import Participant, Blacklist, Draw, DrawResult

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'email']



class BlacklistSerializer(serializers.ModelSerializer):
    participant_email = serializers.EmailField(source='participant.email', read_only=True)
    blocked_participant = serializers.IntegerField(source='blocked_participant.id')

    class Meta:
        model = Blacklist
        fields = ['id', 'participant_email', 'blocked_participant']

    def create(self, validated_data):
        participant_email = self.context['request'].data.get('participant_email')
        blocked_participant_id = self.context['request'].data.get('blocked_participant')

        participant = Participant.objects.get(email=participant_email)
        blocked_participant = Participant.objects.get(id=blocked_participant_id)
        return Blacklist.objects.create(participant=participant, blocked_participant=blocked_participant)

class DrawResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawResult
        fields = ['id', 'giver', 'receiver']

class DrawSerializer(serializers.ModelSerializer):
    results = DrawResultSerializer(many=True, read_only=True)

    class Meta:
        model = Draw
        fields = ['id', 'date', 'results']
