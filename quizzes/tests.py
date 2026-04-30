import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Quiz


def create_quiz(title, seconds_delta = 0):
    return Quiz.objects.create(
        title=title,
        created_at=timezone.now() + datetime.timedelta(seconds=seconds_delta)
    )


class QuizIndexViewTests(TestCase):

    def test_without_quizzes(self):
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_quizzes'], [])
        self.assertContains(response, 'No Quizzes')

    def test_with_quizzes(self):
        quiz1 = create_quiz('Quiz 1 title')
        quiz2 = create_quiz('Quiz 2 title', seconds_delta=1)
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_quizzes'], [quiz2, quiz1])
        self.assertContains(response, quiz1.title)
        self.assertContains(response, quiz2.title)


class QuizDetailViewTests(TestCase):

    def test_with_existing_quiz_without_questions(self):
        quiz = create_quiz('Quiz title')
        response = self.client.get(reverse('quizzes:detail', args=(quiz.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['quiz'], quiz)
        self.assertQuerySetEqual(response.context['questions'], [])
        self.assertContains(response, quiz.title)

    def test_with_not_existing_quiz(self):
        response = self.client.get(reverse('quizzes:detail', args=(1,)))
        self.assertEqual(response.status_code, 404)
