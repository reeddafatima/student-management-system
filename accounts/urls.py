from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProfileUpdateView,
    UsersListView, UserUpdateByAdminView, ForgotPasswordView, ResetConfirmView

)
app_name = "accounts"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("users/", UsersListView.as_view(), name="users_list"),
    path("users/<int:pk>/edit/", UserUpdateByAdminView.as_view(), name="user_edit"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset/<int:uid>/", ResetConfirmView.as_view(), name="reset_confirm"),
]
