from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import TeacherSerializer, CourseCategorySerializer, CourseSerializer, ChapterSerializer
from .models import Teacher, CourseCategory, Student, Course, Chapter
from rest_framework import permissions

# Create your views here.
class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

@csrf_exempt
def teacher_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        teacherData = Teacher.objects.get(email=email, password=password)
    except Teacher.DoesNotExist:
        teacherData = None
    if teacherData:
        return JsonResponse({
            'status': 'success', 
            'data': teacherData, 
            'teacher_id': teacherData.id, 
            'bool': True})
    else:
        return JsonResponse({
            'status': 'failed',
            'data': 'Invalid email or password', 
            'message': 'Login failed',
            'bool': False})

class CourseCategoryList(generics.ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

class CourseCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

#Specific Teacher Course

class TeacherCourseList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(pk = teacher_id)
        return Course.objects.filter(teacher=teacher)

# For each chapter in a course
class ChapterList(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

# Specific Course Chapter
class CourseChapterList(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(pk = course_id)
        return Chapter.objects.filter(course=course)
