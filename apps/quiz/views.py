import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from .models import QuizSet, Question, Option, QuizAttempt
from .serializers import *


class QuizSetListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        quizzes = QuizSet.objects.filter(is_active=True)
        return Response(QuizSetSerializer(quizzes, many=True).data)


class QuizQuestionAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, quiz_id):
        quiz = get_object_or_404(QuizSet, id=quiz_id)
        questions = quiz.questions.all()
        return Response(
            QuestionWithCorrectAnswerSerializer(questions, many=True).data
        )

class QuizSubmitAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, quiz_id):
        quiz = get_object_or_404(QuizSet, id=quiz_id)
        answers = request.data.get("answers", {})

        # device id (header first, fallback to body)
        device_id = (
            request.headers.get("X-DEVICE-ID")
            or request.data.get("device_id")
        )

        score = 0
        result_details = []

        questions = quiz.questions.prefetch_related("options")

        for question in questions:
            selected_option_id = answers.get(str(question.id))
            correct_option = question.options.filter(is_correct=True).first()

            selected_option = None
            is_correct = False
            skipped = False

            if selected_option_id:
                selected_option = question.options.filter(
                    id=selected_option_id
                ).first()

                if selected_option and correct_option:
                    if selected_option.id == correct_option.id:
                        score += 1
                        is_correct = True
            else:
                skipped = True

            result_details.append({
                "question_id": question.id,
                "question_text": question.question_text,
                "selected_option": (
                    {
                        "id": selected_option.id,
                        "text": selected_option.text
                    } if selected_option else None
                ),
                "correct_option": (
                    {
                        "id": correct_option.id,
                        "text": correct_option.text
                    } if correct_option else None
                ),
                "is_correct": is_correct,
                "skipped": skipped
            })

        attempt = QuizAttempt.objects.create(
            user=request.user if request.user.is_authenticated else None,
            quiz_set=quiz,
            score=score,
            total_questions=questions.count(),
        )

        return Response({
            "quiz": quiz.title,
            "device_id": device_id,
            "score": score,
            "total": attempt.total_questions,
            "completed": True,
            "details": result_details
        })

