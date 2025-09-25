from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import Course
from .forms import EnrollmentForm
from accounts.models import User

# ---------------- DASHBOARD ----------------
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['students'] = User.objects.filter(is_active=True)
        return context

    def test_func(self):
        return self.request.user.is_staff

# ---------------- COURSE LIST ----------------
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

# ---------------- COURSE DETAIL ----------------
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

# ---------------- FAVORITE/UNFAVORITE ----------------
def course_favorite(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.is_authenticated:
        if request.user in course.favorites.all():
            course.favorites.remove(request.user)
        else:
            course.favorites.add(request.user)
    return redirect("courses:course_detail", pk=course.pk)

# ---------------- COURSE CRUD ----------------
class CourseCreateView(CreateView):
    model = Course
    fields = ['title', 'description', 'credits']
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

class CourseEditView(UpdateView):
    model = Course
    fields = ['title', 'description', 'credits']
    template_name = 'courses/course_edit.html'
    success_url = reverse_lazy('courses:course_list')

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')

# ---------------- ENROLLMENT VIEW ----------------
class EnrollmentView(UserPassesTestMixin, FormView):
    template_name = "courses/enrollment_form.html"
    form_class = EnrollmentForm
    success_url = reverse_lazy('courses:course_list')  # Redirect to course list

    def form_valid(self, form):
        student = form.cleaned_data['student']
        course = form.cleaned_data['course']
        course.favorites.add(student)  # Example: enrolling = add to favorites
        messages.success(self.request, f"{student.email} enrolled in {course.title}")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff  # Only staff can enroll students
