from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin

class OptionInline(admin.TabularInline):
    model = Option
    extra = 2
    min_num = 2
    max_num = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ("question_text", "quiz_set")
    search_fields = ("question_text",)
    list_filter = ("quiz_set",)
    inlines = [OptionInline]


@admin.register(QuizSet)
class QuizSetAdmin(ModelAdmin):
    list_display = ("title", "total_time", "is_active")
    list_editable = ("is_active",)
    search_fields = ("title",)
    inlines = [QuestionInline]


@admin.register(Option)
class OptionAdmin(ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct",)
@admin.register(QuizAttempt)
class QuizAttemptAdmin(ModelAdmin):
    list_display = ("user", "quiz_set", "score", "completed_at")