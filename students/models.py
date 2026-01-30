from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CLASS_CHOICES = [
    ("LKG", "LKG"),
    ("UKG", "UKG"),
    ("1", "Class 1"),
    ("2", "Class 2"),
    ("3", "Class 3"),
    ("4", "Class 4"),
    ("5", "Class 5"),
    ("6", "Class 6"),
    ("7", "Class 7"),
    ("8", "Class 8"),
    ("9", "Class 9"),
    ("10", "Class 10"),
]

SECTION_CHOICES = [
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
]

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    student_class = models.CharField(max_length=10,choices=CLASS_CHOICES)
    section = models.CharField(max_length=5,choices=SECTION_CHOICES)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
    
class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="parents"
    )
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username    
    
from django.contrib.auth.models import User

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

 
class StudentMarks(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    marks = models.IntegerField()

    class Meta:
        unique_together = ('student', 'exam_name', 'subject')

    def __str__(self):
        return f"{self.student.user.username} - {self.exam_name} - {self.subject}"
    
class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')]
    )
    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"
class ExamTimetable(models.Model):
    exam_name = models.CharField(max_length=50)
    student_class = models.CharField(max_length=10,choices=CLASS_CHOICES)
    section = models.CharField(max_length=5,choices=SECTION_CHOICES)

    subject = models.CharField(max_length=50)
    exam_date = models.DateField()
    day = models.CharField(max_length=15)
    time = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.exam_name} - Class {self.student_class}{self.section} - {self.subject}"
 

class Homework(models.Model):

    date = models.DateField()
    student_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    section = models.CharField(max_length=5, choices=SECTION_CHOICES)
    subject = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return f"Class {self.student_class}-{self.section} | {self.subject}"

from django.db import models

class AboutImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='about_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "About Image"

class DummyPayment(models.Model):
    parent = models.ForeignKey(
        ParentProfile,
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    amount = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("PAID", "Paid")],
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.status}"
    
from django.utils import timezone

class ExamPayment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid")],
        default="Pending"
    )
    payment_id = models.CharField(max_length=100, blank=True)
    paid_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.status}"   

class ExamFee(models.Model):
    class_name = models.CharField(max_length=10, unique=True,choices=CLASS_CHOICES)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Class {self.class_name} - ₹{self.amount}"    
    

from django.db import models
from django.utils import timezone

class MonthlyAttendance(models.Model):
    student = models.ForeignKey(
        "StudentProfile",
        on_delete=models.CASCADE,
        related_name="monthly_attendance"
    )
    month = models.DateField(
        help_text="Use first day of the month (e.g. 2026-01-01)"
    )
    total_days = models.PositiveIntegerField()
    present_days = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "month")
        ordering = ["-month"]

    def __str__(self):
        return f"{self.student.user.username} - {self.month.strftime('%B %Y')}"

