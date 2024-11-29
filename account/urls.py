from django.contrib import admin
from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserProfile,UserPasswordChangeView,SendPasswordEmailView,UserPasswordResetView

urlpatterns = [
    path('register/',UserRegistrationView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('profile/',UserProfile.as_view()),
    path('passChange/',UserPasswordChangeView.as_view()),
    path('send-reset-password-email/',SendPasswordEmailView.as_view()),
    path('reset-password/<uid>/<token>',UserPasswordResetView.as_view())
]