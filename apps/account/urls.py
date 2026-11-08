from .views import *
from django.urls import path

urlpatterns = [
    path('signup/',UserSignupView.as_view(), name='signup'),
    path('login/',UserLoginView.as_view(), name='signup'),
    path("password-reset/request/", RequestPasswordResetView.as_view()),
    path("password-reset/verify/",VerifyResetCodeView.as_view()),
    path("password-reset/complete/",CompletePasswordResetView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("account/deactivate/", DeactivateAccountAPIView.as_view()),
    path("account/delete/", DeleteAccountAPIView.as_view()),
    path("account/profile/update/", UserProfileUpdateAPIView.as_view()),
    path("account/change-password/", ChangePasswordAPIView.as_view()),

]
