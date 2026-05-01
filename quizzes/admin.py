from django.contrib import admin
from .models import Quiz, Question, Choice


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
    fields = ['text']
    show_change_link = True


class QuizAdmin(admin.ModelAdmin):
    fields = ['title', 'description']
    inlines = [QuestionInline]
    list_display = ['title', 'description', 'is_active', 'created_at']
    search_fields = ['title', 'description']


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    fields = ['text', 'is_correct']


class QuestionAdmin(admin.ModelAdmin):
    fields = ['quiz', 'text']
    inlines = [ChoiceInline]
    list_display = ['text', 'quiz', 'created_at']
    search_fields = ['text']


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
