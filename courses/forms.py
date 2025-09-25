from django import forms
from .models import Course
from django import forms
from .models import Course
from accounts.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description"]


class EnrollmentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True), label="Select Student")
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Select Course")
