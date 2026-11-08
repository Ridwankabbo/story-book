from django.urls import path
from .views import (
    QuizSetListAPIView,
    QuizQuestionAPIView,
    QuizSubmitAPIView,
)

urlpatterns = [
    path("quiz-sets/", QuizSetListAPIView.as_view()),
    path("quiz/<int:quiz_id>/questions/", QuizQuestionAPIView.as_view()),
    path("quiz/<int:quiz_id>/submit/", QuizSubmitAPIView.as_view()),
]
