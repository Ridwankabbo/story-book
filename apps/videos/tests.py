from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.models import User
from .models import Poll, PollOption, PollVote


class PollVoteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.poll = Poll.objects.create(question='Favorite color?')
        self.option = PollOption.objects.create(poll=self.poll, text='Blue')

    def test_logged_in_user_can_vote_once_per_poll(self):
        user = User.objects.create_user(email='user1@example.com', password='secret123', full_name='User One')
        self.client.force_authenticate(user=user)

        first = self.client.post('/api/v1/polls/vote/', {
            'poll_id': self.poll.id,
            'option_id': self.option.id,
        }, format='json')
        self.assertEqual(first.status_code, 200)
        self.assertEqual(PollVote.objects.filter(poll=self.poll, user=user).count(), 1)

        second = self.client.post('/api/v1/polls/vote/', {
            'poll_id': self.poll.id,
            'option_id': self.option.id,
        }, format='json')
        self.assertEqual(second.status_code, 400)

    def test_guest_device_can_vote_once_per_poll(self):
        first = self.client.post('/api/v1/polls/vote/', {
            'poll_id': self.poll.id,
            'option_id': self.option.id,
            'device_id': 'device-123',
        }, format='json')
        self.assertEqual(first.status_code, 200)
        self.assertEqual(PollVote.objects.filter(poll=self.poll, device_id='device-123').count(), 1)

        second = self.client.post('/api/v1/polls/vote/', {
            'poll_id': self.poll.id,
            'option_id': self.option.id,
            'device_id': 'device-123',
        }, format='json')
        self.assertEqual(second.status_code, 400)
