from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny as A
class PartnershipInquaryAPIView(APIView):
    permission_classes = [A]
    authentication_classes=[]
    def post(self, request, *args, **kwargs):
        serializer = PartnershipInquarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsletterSubscriptionAPIView(APIView):
    permission_classes = [A]
    authentication_classes=[]
    def post(self, request, *args, **kwargs):
        serializer = NewsletterSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ALHeraKitRequestAPIView(APIView):
    permission_classes = [A]
    authentication_classes=[]
    def post(self, request, *args, **kwargs):
        serializer = ALHeraKitRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
