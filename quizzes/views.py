from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Quiz, Attempt, Question, Choice

def index(request):
    latest_quizzes = Quiz.objects.order_by('-created_at')[:10]
    context = { 'latest_quizzes': latest_quizzes }
    return render(request, 'quizzes/index.html', context)

def detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.annotate(
        choice_count=Count('choice')
    ).filter(
        choice_count__gte=2
    ).order_by('created_at').all()
    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, 'quizzes/detail.html', context)

def attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    answers = []
    for k, v in request.POST.items():
        try:
            question = quiz.question_set.get(pk=int(k))
            choice = question.choice_set.get(pk=int(v))
            answer = { 'question': question, 'choice': choice }
        except (ValueError, Question.DoesNotExist, Choice.DoesNotExist):
            pass
        else:
            answers.append(answer)
    if (len(answers) == 0):
        return HttpResponseRedirect(reverse('quizzes:detail', args=(quiz.id,)))
    attempt = Attempt(quiz=quiz)
    attempt.save()
    for answer in answers:
        attempt.answer_set.create(**answer)
    return HttpResponseRedirect(reverse('quizzes:results', args=(attempt.id,)))

def results(request, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    answers = attempt.answer_set.all()
    return render(request, 'quizzes/results.html', { 'answers': answers })
