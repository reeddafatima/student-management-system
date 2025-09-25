from django.urls import path
from . import views
from .views import EnrollmentView


app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('favorite/<int:pk>/', views.course_favorite, name='course_favorite'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('edit/<int:pk>/', views.CourseEditView.as_view(), name='course_edit'),
    path('delete/<int:pk>/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('enroll/', EnrollmentView.as_view(), name='course_enroll'),
]
