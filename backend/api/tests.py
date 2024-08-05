from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Participant, Blacklist, Draw, DrawResult

class ParticipantTests(APITestCase):
    def test_create_participant(self):
        """
        Ensure we can create a new participant object.
        """
        url = reverse('participant-list')
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Participant.objects.count(), 1)
        self.assertEqual(Participant.objects.get().name, 'John Doe')

    def test_get_participants(self):
        """
        Ensure we can retrieve the list of participants.
        """
        Participant.objects.create(name='John Doe', email='john@example.com')
        Participant.objects.create(name='Jane Doe', email='jane@example.com')
        url = reverse('participant-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

class BlacklistTests(APITestCase):
    def setUp(self):
        self.participant1 = Participant.objects.create(name='John Doe', email='john@example.com')
        self.participant2 = Participant.objects.create(name='Jane Doe', email='jane@example.com')

    def test_create_blacklist(self):
        """
        Ensure we can create a new blacklist entry.
        """
        url = reverse('blacklist-list')
        data = {'participant': self.participant1.id, 'blocked_participant': self.participant2.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blacklist.objects.count(), 1)

class DrawTests(APITestCase):
    def setUp(self):
        self.participant1 = Participant.objects.create(name='John Doe', email='john@example.com')
        self.participant2 = Participant.objects.create(name='Jane Doe', email='jane@example.com')
        self.participant3 = Participant.objects.create(name='Bob Smith', email='bob@example.com')

    def test_perform_draw(self):
        """
        Ensure we can perform a draw and create draw results.
        """
        url = reverse('draw-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Draw.objects.count(), 1)
        self.assertEqual(DrawResult.objects.count(), 3)

    def test_get_draw_history(self):
        """
        Ensure we can retrieve the draw history.
        """
        draw = Draw.objects.create()
        DrawResult.objects.create(draw=draw, giver=self.participant1, receiver=self.participant2)
        DrawResult.objects.create(draw=draw, giver=self.participant2, receiver=self.participant3)
        DrawResult.objects.create(draw=draw, giver=self.participant3, receiver=self.participant1)

        url = reverse('draw-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(len(response.data['results'][0]['results']), 3)

    def test_draw_with_blacklist(self):
        """
        Ensure the draw respects the blacklist.
        """
        Blacklist.objects.create(participant=self.participant1, blocked_participant=self.participant2)

        url = reverse('draw-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        draw_results = DrawResult.objects.filter(draw_id=response.data['id'])
        for result in draw_results:
            if result.giver == self.participant1:
                self.assertNotEqual(result.receiver, self.participant2)
