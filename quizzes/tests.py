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

def create_question(quiz, text, seconds_delta = 0):
    return quiz.question_set.create(
        text=text,
        created_at=timezone.now() + datetime.timedelta(seconds=seconds_delta)
    )

def create_choice(question, text, seconds_delta = 0):
    return question.choice_set.create(
        text=text,
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
        self.assertContains(response, 'No Questions')

    def test_with_existing_quiz_with_questions_without_choices(self):
        quiz = create_quiz('Quiz title')
        create_question(quiz, 'Question text 1')
        create_question(quiz, 'Question text 2', 1)
        response = self.client.get(reverse('quizzes:detail', args=(quiz.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['quiz'], quiz)
        self.assertQuerySetEqual(response.context['questions'], [])
        self.assertContains(response, quiz.title)
        self.assertContains(response, 'No Questions')

    def test_with_existing_quiz_with_questions_with_choices(self):
        """
        Make sure only questions with at least two choices are displayed in ascending order
        """
        quiz = create_quiz('Quiz title')
        questions = []
        for i in range(3):
            questions.append(create_question(quiz, f'Question text {i + 1}', i))
        choices = []
        for question_i, choice_count in zip(range(len(questions)), range(1, len(questions) + 1)):
            choices.append([])
            for i in range(choice_count):
                choices[question_i].append(create_choice(
                    questions[question_i],
                    f'Question {question_i + 1} choice {i + 1}',
                    question_i
                ))
        response = self.client.get(reverse('quizzes:detail', args=(quiz.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['quiz'], quiz)
        self.assertQuerySetEqual(response.context['questions'], questions[1:])
        self.assertContains(response, quiz.title)
        for question in questions[1:]:
            self.assertContains(response, question.text)
        for choice in [c for question_choices in choices[1:] for c in question_choices]:
            self.assertContains(response, choice.text)

    def test_with_non_existing_quiz(self):
        response = self.client.get(reverse('quizzes:detail', args=(1,)))
        self.assertEqual(response.status_code, 404)
