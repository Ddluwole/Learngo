from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import TeacherSerializer, CourseCategorySerializer, CourseSerializer, ChapterSerializer, StudentSerializer, WeeklytaskSerializer, StudentDashboardSerializer, NotificationSerializer
from .models import Teacher, CourseCategory, Student, Course, Chapter, Weeklytask, Notification
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
    
@csrf_exempt
def teacher_change_password(request, teacher_id):
    password = request.POST['password']
    try:
        teacherData = Teacher.objects.get(id=teacher_id)
    except Student.DoesNotExist:
        teacherData = None
    if teacherData:
        Teacher.objects.filter(id=teacher_id).update(password=password)
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})
    
# class TeacherDashboard(generics.RetrieveAPIView):
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherDashboardSerializer


class CourseCategoryList(generics.ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

class CourseCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # def get_queryset(self):
    #     qs =  ().get_queryset()
    #     if 'result' in self.request.GET:
    #         qs = Course.objects.all().order_by('-id')[:4]
    #     return qs

#Specific Teacher Course

class TeacherCourseList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(pk = teacher_id)
        return Course.objects.filter(teacher=teacher)

class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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

class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

# Student data

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


@csrf_exempt
def student_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        studentData = Student.objects.get(email=email, password=password)
    except Student.DoesNotExist:
        studentData = None
    if studentData:
        return JsonResponse({
            'status': 'success', 
            'data': studentData, 
            'student_id': studentData.id, 
            'bool': True})
    else:
        return JsonResponse({
            'status': 'failed',
            'data': 'Invalid email or password', 
            'message': 'Login failed',
            'bool': False})
    
@csrf_exempt
def student_change_password(request, student_id):
    password = request.POST['password']
    try:
        studentData = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        studentData = None
    if studentData:
        Student.objects.filter(id=student_id).update(password=password)
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})
    
class StudentDashboard(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDashboardSerializer

class WeeklytaskList(generics.ListCreateAPIView):
    queryset = Weeklytask.objects.all()
    serializer_class = WeeklytaskSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = Student.objects.get(pk = student_id)
        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(pk = teacher_id)
        return Weeklytask.objects.filter(student=student, teacher=teacher)
    

class StudentWeeklytaskList(generics.ListCreateAPIView):
    queryset = Weeklytask.objects.all()
    serializer_class = WeeklytaskSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = Student.objects.get(pk = student_id)
        #Update Notifications
        Notification.objects.filter(student = student, notif_subject ='assignment').update(notif_read_status = True)
        return Weeklytask.objects.filter(student=student)

# class UpdateTaskStatus(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Weeklytask.objects.all()
#     serializer_class = WeeklytaskSerializer

#     def get_queryset(self):
#         student_id = self.kwargs['student_id']
#         student = Student.objects.get(pk = student_id)
#         teacher_id = self.kwargs['teacher_id']
#         teacher = Teacher.objects.get(pk = teacher_id)
#         return Weeklytask.objects.filter(student=student, teacher=teacher)



@csrf_exempt
def student_change_password(request, student_id):
    password = request.POST['password']
    try:
        studentData = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        studentData = None
    if studentData:
        Student.objects.filter(id=student_id).update(password=password)
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})
    

class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = Student.objects.get(pk = student_id)
        return Notification.objects.filter(student=student)
    
