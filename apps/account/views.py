
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import random
from django.core.cache import cache
from .models import User
from .utils import send_password_reset_code
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import jwt, datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from django.core import signing
User = get_user_model()


class UserSignupView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = {
            "code": status.HTTP_201_CREATED,
            "message": "User created successfully",
            "data": UserCreateSerializer(user).data

        }
        return Response(response_data, status=status.HTTP_201_CREATED)


from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.all_objects.get(email=email)  # 👈 IMPORTANT
        except User.DoesNotExist:
            return Response(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid credentials",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 🔒 Check password manually
        if not user.check_password(password):
            return Response(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid credentials",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 🔒 Now check is_active
        if not user.is_active:
            return Response(
                {
                    "code": status.HTTP_403_FORBIDDEN,
                    "message": "Your account is deactivated. Please contact support.",
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # 🔒 Also block soft-deleted users
        if getattr(user, "is_deleted", False):
            return Response(
                {
                    "code": status.HTTP_403_FORBIDDEN,
                    "message": "Account has been deleted.",
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # ✅ Issue tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserCreateSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class RequestPasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"message": "Email required"}, status=400)

        if not User.objects.filter(email=email).exists():
            return Response({"message": "No user with this email"}, status=400)

        code = f"{random.randint(100000, 999999)}"

        # save OTP for 10 minutes
        cache.set(f"otp_{email}", code, timeout=600)

        send_password_reset_code(email, code)

        return Response({
            "message": "OTP sent to email",
        }, status=200)


class VerifyResetCodeView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        saved = cache.get(f"otp_{email}")

        if not saved or saved != code:
            return Response({"message": "Invalid or expired OTP"}, status=400)

        # OTP is correct → generate short lived token
        token = signing.dumps({"email": email})

        # Allow token usage for few minutes
        cache.set(f"reset_token_{email}", token, timeout=300)

        return Response({
            "message": "OTP verified",
            "reset_token": token
        }, status=200)


class CompletePasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        token = request.data.get("reset_token")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            return Response({"message": "Passwords do not match"}, status=400)

        try:
            data = signing.loads(token, max_age=300)  # 5 min expiry
            email = data["email"]
        except Exception:
            return Response({"message": "Invalid or expired reset token"}, status=400)

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        # wipe tokens
        cache.delete(f"otp_{email}")
        cache.delete(f"reset_token_{email}")

        return Response({
            "message": "Password reset successful"
        }, status=200)



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return Response({"message": "Access token missing"}, status=400)

        access_token = auth_header.split(" ")[1]

        #  Check if already blacklisted
        if cache.get(f"blacklist_{access_token}"):
            return Response(
                {"message": "Already logged out"},
                status=200
            )

        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
            exp = payload.get("exp")
        except Exception:
            return Response({"message": "Invalid token"}, status=400)

        now = datetime.datetime.utcnow()
        remaining = exp - int(now.timestamp())

        cache.set(f"blacklist_{access_token}", True, timeout=max(1, remaining))

        return Response({"message": "Logout successful"}, status=200)

class DeactivateAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeactivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.validated_data["confirm"]:
            return Response(
                {"detail": "Confirmation required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user.is_active = False
        user.save(update_fields=["is_active"])

        return Response(
            {"detail": "Account deactivated successfully"},
            status=status.HTTP_200_OK
        )

class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeleteAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        password = serializer.validated_data["password"]

        # 🔐 Verify password
        if not user.check_password(password):
            return Response(
                {"detail": "Incorrect password"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Soft delete
        user.delete()

        return Response(
            {"detail": "Account deleted successfully"},
            status=status.HTTP_200_OK
        )


class UserProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True  # allow partial update
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Profile updated successfully",
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        # 🔐 Check old password
        if not user.check_password(old_password):
            return Response(
                {"detail": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 🔁 Prevent reuse of same password
        if old_password == new_password:
            return Response(
                {"detail": "New password must be different from old password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Set new password
        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )