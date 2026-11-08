from django.db import models
from apps.account.models import User


class QuizSet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total_time = models.PositiveIntegerField(default=60,help_text="Total quiz time in seconds")
    background_image=models.ImageField(upload_to="quiz/background_images/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz_set = models.ForeignKey(QuizSet, related_name="questions", on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(
        Question, related_name="options", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    """
    logged in + guest both supported
    """
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    device_id  = models.CharField(max_length=100, blank=True, null=True)
    quiz_set = models.ForeignKey(QuizSet, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz_set.title} - {self.score}"
