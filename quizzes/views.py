from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Quiz

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
