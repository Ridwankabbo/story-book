from django.urls import path
from .views import GuardianListView, GuardianDetailView, GuardianIdListView

urlpatterns = [
    path("guardians/", GuardianListView.as_view(), name="guardian-list"),
    path("guardians/ids/", GuardianIdListView.as_view(), name="guardian-id-list"),
    path("guardians/<int:id>/", GuardianDetailView.as_view(), name="guardian-detail"),
]
