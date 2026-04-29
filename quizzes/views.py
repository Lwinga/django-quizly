from django.shortcuts import render
from .models import Quiz

def index(request):
    latest_quizzes = Quiz.objects.order_by('-created_at')[:10]
    context = { 'latest_quizzes': latest_quizzes }
    return render(request, 'quizzes/index.html', context)
