from rest_framework import serializers
from .models import Guardian, Country, GuardianQuestion
from apps.products.serializers import ProductSerializer


class CountrySerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = [
            "id",
            "title",
            "subtitle",
            "photos",
        ]

    def get_photos(self, obj):
        return [
            photo.image.url
            for photo in obj.photos.all()
            if photo.image
        ]

class GuardianListSerializer(serializers.ModelSerializer):
    gadget = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    class Meta:
        model = Guardian
        fields = [
            "id",
            "codename",
            "name",
            "age",
            "nationality",
            "profile_photo",
            "gadget",
        ]
    def get_gadget(self, obj):
        # Access the associated gadget and return only the name field
        if obj.gadget:
            return obj.gadget.title  # Assuming `gadget` is a foreign key field on `Guardian`
        return None

    def get_profile_photo(self, obj):
        return [
            photo.profile_photo.url
            for photo in obj.photos.all()
            if photo.profile_photo
        ]

 
class GuardianDetailSerializer(serializers.ModelSerializer):
    gadget = ProductSerializer(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    country = CountrySerializer(read_only=True)
    questions = serializers.SerializerMethodField()
    class Meta:
        model = Guardian
        fields = "__all__"

    def get_profile_photo(self, obj):
        return [
            photo.profile_photo.url
            for photo in obj.photos.all()
            if photo.profile_photo
        ]

    def get_questions(self, obj):
        return [
            {
                "id": question.id,
                "question": question.question,
                "answer": question.answer,
            }
            for question in obj.questions.all()
        ]
