from django.conf import settings
from django.db import models, transaction
from django.db.utils import IntegrityError


class Video(models.Model):
    VIDEO_TYPE_CHOICES = (
        ("trailer", "Teaser Trailer"),
        ("preview", "Official Preview"),
        ("episode", "Episode"),
    )

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)

    video_type = models.CharField(
        max_length=20,
        choices=VIDEO_TYPE_CHOICES
    )

    duration = models.CharField(max_length=10)  # e.g. 2:10

    # 👇 ACTUAL VIDEO FILE
    video_file = models.FileField(
        upload_to="videos/files/"
    )

    thumbnail = models.ImageField(
        upload_to="videos/thumbnails/"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.db.models import Q
##QUiz Models
class Poll(models.Model):
    question = models.CharField(max_length=255)
    poll_of_week = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['poll_of_week'],
                condition=Q(poll_of_week=True),
                name='only_one_weekly_poll'
            )
        ]

    def save(self, *args, **kwargs):
        if self.poll_of_week:
            with transaction.atomic():
                Poll.objects.filter(
                    poll_of_week=True
                ).exclude(
                    pk=self.pk
                ).update(
                    poll_of_week=False
                )
                try:
                    super().save(*args, **kwargs)
                except IntegrityError:
                    Poll.objects.filter(
                        poll_of_week=True
                    ).exclude(
                        pk=self.pk
                    ).update(
                        poll_of_week=False
                    )
                    if self.pk:
                        Poll.objects.filter(pk=self.pk).update(poll_of_week=True)
                    else:
                        super().save(*args, **kwargs)
            return

        super().save(*args, **kwargs)

    def __str__(self):
        return self.question


class PollOption(models.Model):
    poll = models.ForeignKey(
        Poll, related_name="options", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='poll_votes'
    )
    device_id = models.CharField(max_length=100, blank=True, null=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("poll", "user"), ("poll", "device_id"))

    def __str__(self):
        return f"{self.poll} -> {self.option}"


class classroomData(models.Model):
    types=models.CharField(max_length=120,choices=(('reading_guide','Reading Guide'),('classroom_activity','Classroom Activity'),('sample_chapter','Sample Chapter')))
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image=models.ImageField(upload_to="classroom/images/")
    pdf=models.FileField(upload_to="classroom/pdfs/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class MiniGameBakgroudn(models.Model):
    image=models.ImageField(upload_to="minigame/images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Game Background"