from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ---------------- PUBLIC ----------------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.student_logout, name='logout'),

    # ---------------- STUDENT ----------------
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('marks/<str:exam_name>/', views.marks_by_exam, name='marks_by_exam'),
    path('attendance/', views.attendance, name='attendance'),
    path('homework/', views.homework_view, name='homework'),
    path('exam-timetable/', views.exam_timetable_view, name='exam_timetable'),

    # ---------------- TEACHER ----------------
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/homework/add/', views.teacher_add_homework, name='teacher_add_homework'),
    path('teacher/attendance/', views.mark_attendance, name='teacher_mark_attendance'),
    path('teacher/marks/', views.teacher_marks, name='teacher_marks'),

    # ---------------- PARENT ----------------
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('parent/pay/', views.dummy_pay_exam_fee, name='dummy_pay_exam_fee'),
    path('parent/payment-history/', views.payment_history, name='payment_history'),
    path('parent/receipt/<int:pk>/', views.payment_receipt, name='payment_receipt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"