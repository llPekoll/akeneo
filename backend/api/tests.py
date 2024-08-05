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
        data = {
            'participant_email': 'john@example.com',
            'blocked_participant_email': 'jane@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blacklist.objects.count(), 1)
        self.assertEqual(Blacklist.objects.get().participant, self.participant1)
        self.assertEqual(Blacklist.objects.get().blocked_participant, self.participant2)


class DrawTests(APITestCase):
    def setUp(self):
        self.participant1 = Participant.objects.create(name='John Doe', email='john@example.com')
        self.participant2 = Participant.objects.create(name='Jane Doe', email='jane@example.com')
        self.participant3 = Participant.objects.create(name='Bob Smith', email='bob@example.com')

    def test_draw_with_blacklist(self):
        """
        Ensure the draw respects the blacklist.
        """
        # Create a blacklist entry
        Blacklist.objects.create(participant=self.participant1, blocked_participant=self.participant2)

        url = reverse('draw-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        results = response.data['results']
        for result in results:
            if result['giver_email'] == 'john@example.com':
                self.assertNotEqual(result['receiver_email'], 'jane@example.com')

    def test_draw_with_complex_blacklist(self):
        """
        Test a more complex blacklist scenario.
        """
        Participant.objects.create(name='Alice', email='alice@example.com')
        Participant.objects.create(name='Charlie', email='charlie@example.com')

        # Create multiple blacklist entries
        Blacklist.objects.create(participant=self.participant1, blocked_participant=self.participant2)
        Blacklist.objects.create(participant=self.participant2, blocked_participant=self.participant3)
        Blacklist.objects.create(participant=self.participant3, blocked_participant=self.participant1)

        url = reverse('draw-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        results = response.data['results']
        for result in results:
            if result['giver_email'] == 'john@example.com':
                self.assertNotEqual(result['receiver_email'], 'jane@example.com')
            if result['giver_email'] == 'jane@example.com':
                self.assertNotEqual(result['receiver_email'], 'bob@example.com')
            if result['giver_email'] == 'bob@example.com':
                self.assertNotEqual(result['receiver_email'], 'john@example.com')

    def test_impossible_draw(self):
        """
        Test that the draw fails when it's impossible to satisfy all blacklist constraints.
        """
        # Create a situation where it's impossible to satisfy all constraints
        Blacklist.objects.create(participant=self.participant1, blocked_participant=self.participant2)
        Blacklist.objects.create(participant=self.participant1, blocked_participant=self.participant3)
        Blacklist.objects.create(participant=self.participant2, blocked_participant=self.participant1)
        Blacklist.objects.create(participant=self.participant2, blocked_participant=self.participant3)

        url = reverse('draw-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Unable to complete draw. Please try again or adjust blacklist.")
