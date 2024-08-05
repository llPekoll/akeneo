from rest_framework import viewsets, response
from .models import Participant, Blacklist, Draw, DrawResult
from .serializers import ParticipantSerializer, BlacklistSerializer, DrawSerializer
import random

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class BlacklistViewSet(viewsets.ModelViewSet):
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer

class DrawViewSet(viewsets.ModelViewSet):
    queryset = Draw.objects.all().order_by('-date')[:5]
    serializer_class = DrawSerializer

    def create(self, request):
        participants = list(Participant.objects.all())
        draw = Draw.objects.create()
        available_receivers = participants.copy()
        for giver in participants:
            blacklist = Blacklist.objects.filter(participant=giver).values_list('blocked_participant', flat=True)
            valid_receivers = [r for r in available_receivers if r != giver and r.id not in blacklist]
            if not valid_receivers:
                # If no valid receivers, reset the draw
                DrawResult.objects.filter(draw=draw).delete()
                draw.delete()
                return response.Response({"error": "Unable to complete draw. Please try again."}, status=400)
            receiver = random.choice(valid_receivers)
            DrawResult.objects.create(draw=draw, giver=giver, receiver=receiver)
            available_receivers.remove(receiver)

        serializer = self.get_serializer(draw)
        return response.Response(serializer.data, status=201)
