from django.urls import path
from .views import TeacherList, TeacherDetail, teacher_login, CourseCategoryList, CourseList, TeacherCourseList, ChapterList, CourseChapterList

urlpatterns = [
    path('teacher/', TeacherList.as_view()),
    path('teacher/<int:pk>/', TeacherDetail.as_view()),
    path('teacher/login/', teacher_login),

    #category
    path('category/', CourseCategoryList.as_view()),

    # course
    path('course/', CourseList.as_view()),

    # Teacher Course
    path('teacher-courses/<int:teacher_id>/', TeacherCourseList.as_view()),

    # Chapter
    path('chapter/', ChapterList.as_view()),

    # Specific Course Chapter
    path('course-chapters/<int:course_id>/', CourseChapterList.as_view()),


]