from django.contrib import admin
from django.conf import settings

# =========================
# IMPORT MODELS
# =========================
from .models import (
    StudentProfile,
    ParentProfile,
    TeacherProfile,
    StudentMarks,
    Attendance,
    ExamTimetable,
    Homework,
    AboutImage,
    ExamFee,
)

# =========================
# ADMIN SITE BRANDING
# =========================
admin.site.site_header = settings.SCHOOL_INFO["NAME"]
admin.site.site_title = settings.SCHOOL_INFO["NAME"]
admin.site.index_title = "Administration Panel"

# =========================
# SIMPLE REGISTRATIONS
# =========================
admin.site.register(Attendance)
admin.site.register(TeacherProfile)
admin.site.register(ExamFee)

# =========================
# STUDENT PROFILE ADMIN
# =========================
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "student_class",
        "section",
        "phone",
    )
    list_filter = (
        "student_class",
        "section",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )

# =========================
# PARENT PROFILE ADMIN
# =========================
@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "student",
        "get_student_class",
        "get_student_section",
        "phone",
    )
    list_filter = (
        "student__student_class",
        "student__section",
    )
    search_fields = (
        "user__username",
        "student__user__username",
        "student__user__first_name",
        "student__user__last_name",
    )

    def get_student_class(self, obj):
        return obj.student.student_class
    get_student_class.short_description = "Class"

    def get_student_section(self, obj):
        return obj.student.section
    get_student_section.short_description = "Section"

# =========================
# EXAM TIMETABLE ADMIN
# =========================
@admin.register(ExamTimetable)
class ExamTimetableAdmin(admin.ModelAdmin):
    list_display = (
        "exam_name",
        "student_class",
        "section",
        "subject",
        "exam_date",
        "day",
        "time",
    )
    list_filter = (
        "exam_name",
        "student_class",
        "section",
    )
    search_fields = (
        "exam_name",
        "subject",
    )

# =========================
# STUDENT MARKS ADMIN
# =========================
@admin.register(StudentMarks)
class StudentMarksAdmin(admin.ModelAdmin):
    list_filter = (
        "student__student_class",
        "student__section",
        "exam_name",
        "subject",
    )

# =========================
# HOMEWORK ADMIN
# =========================
@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "subject",
    )
    list_filter = (
        "date",
        "subject",
    )
    search_fields = (
        "subject",
    )

# =========================
# ABOUT PAGE IMAGES ADMIN
# =========================
@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
    )

from .models import MonthlyAttendance

@admin.register(MonthlyAttendance)
class MonthlyAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "get_class",
        "get_section",
        "month",
        "total_days",
        "present_days",
    )
    list_filter = (
        "month",
        "student__student_class",
        "student__section",
    )
    search_fields = (
        "student__user__username",
        "student__user__first_name",
        "student__user__last_name",
    )

    def get_class(self, obj):
        return obj.student.student_class
    get_class.short_description = "Class"

    def get_section(self, obj):
        return obj.student.section
    get_section.short_description = "Section"

