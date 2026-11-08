from rest_framework import serializers
from .models import *


class VideoSerializer(serializers.ModelSerializer):
    video_file = serializers.FileField()
    thumbnail = serializers.ImageField()

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "subtitle",
            "video_type",
            "duration",
            "video_file",
            "thumbnail",
        ]

class PollSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ["id", "question", "options","created_at"]

    def get_options(self, poll):
        total_votes = poll.pollvote_set.count()
        result = []

        for option in poll.options.all():
            votes = option.pollvote_set.count()
            percentage = (votes / total_votes * 100) if total_votes else 0

            result.append({
                "id": option.id,
                "text": option.text,
                "votes": votes,
                "percentage": round(percentage, 1),
            })

        return result


class ClassroomDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = classroomData
        fields = [
            "id",
            "types",
            "title",
            "subtitle",
            "description",
            "image",
            "pdf",
            "created_at",
        ]

class MiniGameBakgroudnSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniGameBakgroudn
        fields = [
            "id",
            "image",
            "created_at",
        ]
