import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Quiz


class QuizIndexViewTests(TestCase):

    def test_without_quizzes(self):
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_quizzes'], [])
        self.assertContains(response, 'No Quizzes')

    def test_with_quizzes(self):
        now = timezone.now()
        quiz1 = Quiz.objects.create(title='Quiz 1 title', created_at=now)
        quiz2 = Quiz.objects.create(
            title='Quiz 2 title',
            created_at=now + datetime.timedelta(seconds=1)
        )
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_quizzes'], [quiz2, quiz1])
        self.assertContains(response, quiz1.title)
        self.assertContains(response, quiz2.title)
