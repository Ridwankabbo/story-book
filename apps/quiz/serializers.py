from rest_framework import serializers
from .models import QuizSet, Question, Option, QuizAttempt


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text"]


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "options"]



class QuizSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSet
        fields = ["id", "title", "description", "total_time","background_image"]

class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = "__all__"

class QuestionWithCorrectAnswerSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    correct_ans = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ["id", "question_text", "correct_ans", "options"]

    def get_correct_ans(self, obj):
        correct_option = obj.options.filter(is_correct=True).first()
        if correct_option:
            return {
                "id": correct_option.id,
                "text": correct_option.text
            }
        return None
