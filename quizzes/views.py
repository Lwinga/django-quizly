from django.shortcuts import render, get_object_or_404
from .models import Quiz

def index(request):
    latest_quizzes = Quiz.objects.order_by('-created_at')[:10]
    context = { 'latest_quizzes': latest_quizzes }
    return render(request, 'quizzes/index.html', context)

def detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    context = {
        'quiz': quiz,
        'questions': quiz.question_set.order_by('created_at').all()
    }
    return render(request, 'quizzes/detail.html', context)
