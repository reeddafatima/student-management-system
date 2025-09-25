from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import ListView
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
import random

from .models import User
from .forms import (
    UserRegistrationForm, LoginForm, ProfileUpdateForm,
    PasswordResetRequestForm, SetPasswordWithOTPForm
)

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        messages.success(self.request, "Welcome back!")
        return redirect("/")

class LogoutView(FormView):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out.")
        return redirect("accounts:login")

class ForgotPasswordView(FormView):
    template_name = "accounts/forgot_password.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(self.request, "If that email exists we sent an OTP (no leak).")
            return super().form_valid(form)

        otp = f"{random.randint(0, 999999):06d}"
        user.otp = otp
        user.save(update_fields=["otp"])

        send_mail(
            subject="Your OTP for password reset",
            message=f"Your OTP is {otp}. Use it to reset your password.",
            from_email="no-reply@example.com",
            recipient_list=[email],
            fail_silently=False,
        )
        messages.success(self.request, "OTP sent to your email. Use it to reset password.")
        return redirect("accounts:reset_confirm", uid=user.id)

class ResetConfirmView(FormView):
    template_name = "accounts/reset_confirm.html"
    form_class = SetPasswordWithOTPForm
    success_url = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        self.uid = kwargs.get("uid")
        self.user = get_object_or_404(User, id=self.uid)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        otp = form.cleaned_data["otp"]
        if self.user.otp != otp:
            form.add_error("otp", "Invalid OTP")
            return self.form_invalid(form)
        self.user.set_password(form.cleaned_data["new_password1"])
        self.user.otp = ""
        self.user.save()
        messages.success(self.request, "Password reset successful. Please login.")
        return super().form_valid(form)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("courses:course_list")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

class UsersListView(UserPassesTestMixin, ListView):
    model = User
    template_name = "accounts/users_list.html"
    context_object_name = "users"
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_staff

class UserUpdateByAdminView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:users_list")

    def test_func(self):
        return self.request.user.is_staff
