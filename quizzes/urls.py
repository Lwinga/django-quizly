from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:quiz_id>/', views.detail, name='detail'),
]