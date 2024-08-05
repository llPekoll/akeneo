from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Participant, Blacklist, Draw, DrawResult
from .serializers import ParticipantSerializer, BlacklistSerializer, DrawSerializer
import random
from rest_framework.decorators import action

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class DrawViewSet(viewsets.ModelViewSet):
    queryset = Draw.objects.all().order_by('-date')[:5]
    serializer_class = DrawSerializer

    def create(self, request):
        participants = list(Participant.objects.all())
        if len(participants) < 2:
            return Response({"error": "Not enough participants for a draw."}, status=status.HTTP_400_BAD_REQUEST)

        draw = Draw.objects.create()

        available_receivers = participants.copy()
        for giver in participants:
            blacklist = Blacklist.objects.filter(participant=giver).values_list('blocked_participant', flat=True)
            valid_receivers = [r for r in available_receivers if r != giver and r.id not in blacklist]

            if not valid_receivers:
                # If no valid receivers, reset the draw
                DrawResult.objects.filter(draw=draw).delete()
                draw.delete()
                return Response({"error": "Unable to complete draw. Please try again or adjust blacklist."}, status=status.HTTP_400_BAD_REQUEST)

            receiver = random.choice(valid_receivers)
            DrawResult.objects.create(draw=draw, giver=giver, receiver=receiver)
            available_receivers.remove(receiver)

        serializer = self.get_serializer(draw)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BlacklistViewSet(viewsets.ModelViewSet):
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['delete'], url_path='blacklist/(?P<participant_id>[^/.]+)/(?P<email>[^/.]+)')
    def remove_blacklist(self, request, participant_id=None, email=None):
        try:
            blacklist_entry = Blacklist.objects.get(participant_id=participant_id, email=email)
            blacklist_entry.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Blacklist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)