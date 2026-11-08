from django.urls import path, include
from  .views import *
urlpatterns = [
    path('videos/',VideoListAPIView.as_view(), name='video-list'),
    path("polls/", PollListAPIView.as_view()),       # GET all polls
    path("polls/vote/", PollVoteAPIView.as_view()),
    path("polls/<int:pk>/results/", PollResultsAPIView.as_view()),  # GET results for a specific poll
    path("poll-of-week/", PollOfWeek.as_view(), name='poll-of-week'),
    path('videos/<int:pk>/', VideoDetailAPIView.as_view(), name='video-detail'),
    path('classroom/<str:classroom_type>/', ClassroomDataAPIView.as_view(), name='classroom-data'),
    path('classroom_data/all/', ClassroomDataAllAPIView.as_view(), name='classroom-data-all'),
    path('minigame_backgrounds/', MiniGameBakgroudnAPIView.as_view(), name='minigame-backgrounds'),
]