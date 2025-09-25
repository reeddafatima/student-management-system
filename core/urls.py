from django.contrib import admin
from django.urls import path, include
from courses.views import CourseListView   
from courses.views import DashboardView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("courses/", include("courses.urls")),
    path("", CourseListView.as_view(), name="home"),  
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
