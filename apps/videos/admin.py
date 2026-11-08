from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin

@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = ("id", "title", "uploaded_at")

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 2  # show 2 empty option fields by default


@admin.register(Poll)
class PollAdmin(ModelAdmin):
    list_display = ("id", "question","poll_of_week","created_at")
    inlines = [PollOptionInline]


@admin.register(classroomData)
class ClassroomDataAdmin(ModelAdmin):
    list_display = ("title", "types", "created_at")


@admin.register(MiniGameBakgroudn)
class MiniGameBakgroudnAdmin(ModelAdmin):
    list_display = ("id","image", "created_at")
    

