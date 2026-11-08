from rest_framework import generics
from rest_framework.response import Response
from .models import Guardian
from rest_framework.permissions import AllowAny as A
from .serializers import (
    GuardianListSerializer,
    GuardianDetailSerializer
)


class GuardianListView(generics.ListAPIView):
    queryset = Guardian.objects.all()
    serializer_class = GuardianListSerializer
    permission_classes = [A]


class GuardianDetailView(generics.RetrieveAPIView):
    queryset = Guardian.objects.all()
    serializer_class = GuardianDetailSerializer
    lookup_field = "id"
    permission_classes = [A]


class GuardianIdListView(generics.ListAPIView):
    queryset = Guardian.objects.all()
    permission_classes = [A]

    def list(self, request, *args, **kwargs):
        ids = list(self.get_queryset().values_list("id", flat=True))
        return Response(ids)
