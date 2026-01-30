# ===============================
# IMPORTS (CLEANED)
# ===============================

from collections import defaultdict
from datetime import datetime
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import (
    StudentProfile,
    ParentProfile,
    TeacherProfile,
    StudentMarks,
    Attendance,
    MonthlyAttendance,
    Homework,
    ExamTimetable,
    ExamFee,
    ExamPayment,
    AboutImage,
)

from .forms import StudentProfileForm, HomeworkForm
from .utils import teacher_required, student_required, parent_required


logger = logging.getLogger("students")


# ===============================
# PUBLIC PAGES
# ===============================

def home(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Teacher").exists():
            return redirect("teacher_dashboard")
        if request.user.groups.filter(name="Parent").exists():
            return redirect("parent_dashboard")

    school_details = {
        "School_name": "Gnanodhaya Grammer High School",
        "Location": "Hyderabad",
        "Principal": "Ms. Sharadha",
    }
    return render(request, "students/home.html", school_details)


def about(request):
    images = AboutImage.objects.all()
    return render(request, "students/about.html", {"images": images})


def contact(request):
    return render(request, "students/contact.html")


# ===============================
# LOGIN / LOGOUT
# ===============================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if hasattr(user, "parentprofile"):
                return redirect("parent_dashboard")
            if hasattr(user, "teacherprofile"):
                return redirect("teacher_dashboard")
            if hasattr(user, "studentprofile"):
                return redirect("home")

            return redirect("home")

        return render(request, "students/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "students/login.html")


def student_logout(request):
    logout(request)
    return redirect("login")


# ===============================
# STUDENT SECTION
# ===============================

@login_required
@student_required
def profile(request):
    profile = StudentProfile.objects.filter(user=request.user).first()

    return render(request, "students/profile.html", {
        "user": request.user,
        "profile": profile
    })


@login_required
@student_required
def edit_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == "POST":
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, "students/edit_profile.html", {"form": form})


@login_required
@student_required
def attendance(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    attendance_records = Attendance.objects.filter(
        student=student_profile
    ).order_by("-date")

    total_days = attendance_records.count()
    present_days = attendance_records.filter(status="Present").count()
    absent_days = attendance_records.filter(status="Absent").count()

    monthly_attendance = MonthlyAttendance.objects.filter(
        student=student_profile
    ).order_by("-month")

    return render(request, "students/attendance.html", {
        "attendance": attendance_records,
        "total_days": total_days,
        "present_days": present_days,
        "absent_days": absent_days,
        "monthly_attendance": monthly_attendance,
    })


@login_required
@student_required
def homework_view(request):
    profile = get_object_or_404(StudentProfile, user=request.user)

    homeworks = Homework.objects.filter(
        student_class=profile.student_class,
        section=profile.section
    ).order_by("-date")

    return render(request, "students/homework.html", {
        "homeworks": homeworks
    })


@login_required
@student_required
def exam_timetable_view(request):
    profile = get_object_or_404(StudentProfile, user=request.user)

    timetables = ExamTimetable.objects.filter(
        student_class=profile.student_class,
        section=profile.section
    ).order_by("exam_date")

    return render(request, "students/exam_timetable.html", {
        "timetables": timetables
    })


# ===============================
# MARKS (CORE LOGIC UNCHANGED)
# ===============================

@login_required
@student_required
def marks_by_exam(request, exam_name):
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    logger.info(
        "Marks page opened | user=%s | exam=%s",
        request.user.username,
        exam_name
    )

    if exam_name in ["SA-1", "SA-2"]:
        fa_exams = ["FA-1", "FA-2"] if exam_name == "SA-1" else ["FA-3", "FA-4"]

        logger.info(
            "SA calculation | user=%s | exam=%s | FA exams=%s",
            request.user.username,
            exam_name,
            ",".join(fa_exams)
        )

        sa_marks_qs = StudentMarks.objects.filter(
            student=student_profile,
            exam_name=exam_name
        )

        fa_marks_qs = StudentMarks.objects.filter(
            student=student_profile,
            exam_name__in=fa_exams
        )

        fa_totals = defaultdict(int)
        for m in fa_marks_qs:
            fa_totals[m.subject] += m.marks

        marks_list = []
        total_marks = 0

        for sa in sa_marks_qs:
            fa_total = fa_totals.get(sa.subject, 0)
            subject_total = fa_total + sa.marks

            sa.fa_total = fa_total
            sa.total = subject_total

            total_marks += subject_total
            marks_list.append(sa)

        subject_count = len(marks_list)
        max_marks = subject_count * 100
        percentage = round((total_marks / max_marks) * 100, 2) if max_marks else 0

    else:
        marks_list = StudentMarks.objects.filter(
            student=student_profile,
            exam_name=exam_name
        )

        total_marks = sum(m.marks for m in marks_list)
        subject_count = marks_list.count()
        max_marks = subject_count * 20
        percentage = round((total_marks / max_marks) * 100, 2) if max_marks else 0

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    else:
        grade = "Fail"

    return render(request, "students/marks.html", {
        "exam_name": exam_name,
        "marks_list": marks_list,
        "total": total_marks,
        "percentage": percentage,
        "grade": grade,
    })


# ===============================
# TEACHER SECTION
# ===============================

def teacher_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user and user.groups.filter(name="Teacher").exists():
            login(request, user)
            return redirect("teacher_dashboard")

        return render(request, "teachers/teacher_login.html", {
            "error": "Invalid teacher credentials"
        })

    return render(request, "teachers/teacher_login.html")


@login_required
@teacher_required
def teacher_dashboard(request):
    return render(request, "teachers/dashboard.html")


@login_required
@teacher_required
def teacher_add_homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Homework added successfully")
            return redirect("teacher_dashboard")
    else:
        form = HomeworkForm()

    return render(request, "teachers/add_homework.html", {"form": form})


@login_required
@teacher_required
def mark_attendance(request):
    students = None
    attendance_map = {}
    class_name = section = selected_date = ""

    if request.method == "GET" and "load" in request.GET:
        
        class_name = request.GET.get("class")
        section = request.GET.get("section")
        selected_date = request.GET.get("date")

        students = StudentProfile.objects.filter(
            student_class=class_name,
            section=section
        )

        attendance_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

        existing_records = Attendance.objects.filter(
            student__in=students,
            date=attendance_date
        )

        attendance_map = {
            r.student.id: r.status for r in existing_records
        }

    if request.method == "POST":
        try:
            class_name = request.POST.get("class")
            section = request.POST.get("section")
            selected_date = request.POST.get("date")

            students = StudentProfile.objects.filter(
                student_class=class_name,
                section=section
            )

            attendance_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

            for student in students:
                status = request.POST.get(f"status_{student.id}")
                if status:
                    Attendance.objects.update_or_create(
                        student=student,
                        date=attendance_date,
                        defaults={"status": status}
                    )

            messages.success(request, "Attendance saved")
            return redirect("teacher_dashboard")
        except Exception as e:
            logger.error(
                "Attendance save failed | teacher=%s | error=%s",
                request.user.username,
                str(e),
                exc_info=True
            )
            messages.error(request, "Failed to save attendance.")

    return render(request, "teachers/mark_attendance.html", {
        "students": students,
        "attendance_map": attendance_map,
        "class_name": class_name,
        "section": section,
        "selected_date": selected_date
    })


@login_required
@teacher_required
def teacher_marks(request):
    students = marks_map = None
    class_name = section = subject = exam_name = ""

    if request.method == "GET" and "load" in request.GET:
        class_name = request.GET.get("class")
        section = request.GET.get("section")
        subject = request.GET.get("subject")
        exam_name = request.GET.get("exam_name")

        students = StudentProfile.objects.filter(
            student_class=class_name,
            section=section
        )

        existing_marks = StudentMarks.objects.filter(
            student__in=students,
            subject=subject,
            exam_name=exam_name
        )

        marks_map = {
            m.student.id: m.marks for m in existing_marks
        }

    if request.method == "POST":
        class_name = request.POST.get("class")
        section = request.POST.get("section")
        subject = request.POST.get("subject")
        exam_name = request.POST.get("exam_name")

        students = StudentProfile.objects.filter(
            student_class=class_name,
            section=section
        )

        for student in students:
            marks = request.POST.get(f"marks_{student.id}")
            if marks:
                StudentMarks.objects.update_or_create(
                    student=student,
                    subject=subject,
                    exam_name=exam_name,
                    defaults={"marks": marks}
                )

        messages.success(request, "Marks saved successfully")
        return redirect("teacher_dashboard")

    return render(request, "teachers/add_marks.html", {
        "students": students,
        "marks_map": marks_map,
        "class_name": class_name,
        "section": section,
        "subject": subject,
        "exam_name": exam_name
    })


# ===============================
# PARENT SECTION
# ===============================

@login_required
@parent_required
def parent_dashboard(request):
    parent = request.user.parentprofile
    student = parent.student

    fee_obj = ExamFee.objects.filter(
        class_name=student.student_class
    ).first()

    total_fee = fee_obj.amount if fee_obj else 0

    payment = ExamPayment.objects.filter(student=student).first()
    paid_amount = payment.amount if payment else 0

    return render(request, "parents/dashboard.html", {
        "student": student,
        "total_fee": total_fee,
        "paid_amount": paid_amount,
        "remaining_amount": total_fee - paid_amount,
        "payment": payment,
    })


@login_required
@parent_required
def dummy_pay_exam_fee(request):
    parent = request.user.parentprofile
    student = parent.student

    fee_obj = ExamFee.objects.filter(
        class_name=student.student_class
    ).first()

    total_fee = fee_obj.amount if fee_obj else 0

    if request.method == "POST":
        try:
            amount_str = request.POST.get("pay_amount")

            if not amount_str:
                return redirect("parent_dashboard")
        
            pay_amount = int(request.POST.get("pay_amount", 0))

            payment, _ = ExamPayment.objects.get_or_create(
                student=student,
                defaults={"amount": 0, "status": "Pending"}
            )

            remaining = total_fee - payment.amount
            pay_amount = min(pay_amount, remaining)

            payment.amount += pay_amount
            payment.status = "Paid" if payment.amount >= total_fee else "Partial"
            payment.payment_id = f"DUMMY-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            payment.paid_on = timezone.now()
            payment.save()

            logger.info(
                "Payment success | parent=%s | student=%s | amount=%s",
                request.user.username,
                student.user.username,
                pay_amount
            )

            return render(request, "parents/payment_success.html", {
                "student": student,
                "paid_amount": pay_amount,
                "payment": payment,
                "remaining": total_fee - payment.amount
            })
        except Exception as e:
            logger.error(
                "Payment failed | parent=%s | student=%s | error=%s",
                request.user.username,
                student.user.username,
                str(e),
                exc_info=True
            )
            messages.error(request, "Payment failed. Please try again.")
            return redirect("parent_dashboard")


    return render(request, "parents/pay_exam_fee.html")


@login_required
@parent_required
def payment_history(request):
    parent = request.user.parentprofile
    student = parent.student

    payments = ExamPayment.objects.filter(
        student=student
    ).order_by("-paid_on")

    return render(request, "parents/payment_history.html", {
        "student": student,
        "payments": payments
    })


@login_required
@parent_required
def payment_receipt(request, pk):
    payment = get_object_or_404(ExamPayment, id=pk)
    return render(request, "parents/payment_receipt.html", {
        "payment": payment
    })
