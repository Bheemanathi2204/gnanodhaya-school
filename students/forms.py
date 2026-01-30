from django import forms
from .models import StudentMarks
from .models import StudentProfile
from .models import Homework

class StudentMarksForm(forms.ModelForm):
    class Meta:
        model = StudentMarks
        fields = ['student', 'exam_name', 'subject', 'marks']
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['roll_number', 'student_class', 'section', 'phone']

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['date', 'student_class', 'section', 'subject', 'details']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'details': forms.Textarea(attrs={'rows': 4}),
        }

from .models import Attendance
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

