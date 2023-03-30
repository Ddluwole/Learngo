from django.urls import path
from .views import TeacherList, TeacherDetail, teacher_login, teacher_change_password, student_change_password, CourseCategoryList, CourseList, TeacherCourseList, ChapterList, CourseChapterList, TeacherCourseDetail, ChapterDetail, StudentList, StudentDetail, student_login, WeeklytaskList, StudentWeeklytaskList,  NotificationList,TeacherRegisterView, student_register, TeacherVerifyEmail, TeacherLoginView, PasswordTokenCheckAPI, TeacherPasswordResetView, SetNewPasswordAPIView, LogoutAPIView

urlpatterns = [
    path('teacher-list/', TeacherList.as_view()),
    path('teacher-register/', TeacherRegisterView.as_view()),
    path('verify-email/',TeacherVerifyEmail.as_view(), name='verify-email'),
    path('teacher-login/', TeacherLoginView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('request-reset-password/', TeacherPasswordResetView.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'), 
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),

    path('student-register/', student_register),    
    path('teacher/<int:pk>/', TeacherDetail.as_view()),
     # Teacher Course
    path('teacher-courses/<int:teacher_id>/', TeacherCourseList.as_view()),
    # path('teacher-login/', teacher_login),
    path('teacher/change-password/<int:teacher_id>/', teacher_change_password),
    

    #category
    path('category/', CourseCategoryList.as_view()),

    # course
    path('course/', CourseList.as_view()),

   

    # Chapter
    path('chapter/', ChapterList.as_view()),

    # Specific Course Chapter
    path('course-chapters/<int:course_id>/', CourseChapterList.as_view()),

    path('chapter/<int:pk>', ChapterDetail.as_view()),

    path('teacher-course-detail/<int:pk>', TeacherCourseDetail.as_view()),

    path('student-list/', StudentList.as_view()),    
    path('student-login/', student_login),
    path('student/change-password/<int:student_id>/', student_change_password),
    path('student/<int:pk>/', StudentDetail.as_view()),

    path('weekly-task/<int:student_id>/<int:teacher_id>', WeeklytaskList.as_view()),

    path('weekly-task/<int:student_id>/', StudentWeeklytaskList.as_view()),

    # path('update-task-status/<int:pk>/', UpdateTaskStatus.as_view()),

    path('my-notifications/<int:student_id>/', NotificationList.as_view()),


]