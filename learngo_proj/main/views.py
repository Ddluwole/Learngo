from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from .serializers import TeacherSerializer, CourseCategorySerializer, CourseSerializer, ChapterSerializer, StudentSerializer, WeeklytaskSerializer, StudentDashboardSerializer, NotificationSerializer, TeacherRegistrationSerializer, StudentRegistrationSerializer, TeacherEmailVerificationSerializer, TeacherLoginSerializer, TeacherSetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, LogoutSerializer
from .models import Teacher, CourseCategory, Student, Course, Chapter, Weeklytask, Notification
from rest_framework.decorators import api_view
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.
class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer



    

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherRegisterView(generics.GenericAPIView):
    serializer_class = TeacherRegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = Teacher.objects.get(email = user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('verify-email')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi ' + user.first_name + ', Use the link below to verify your email \n'+ absurl
        data = {'email_body': email_body, 'email_subject': 'Verify your email', 'to_email': user.email}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class TeacherVerifyEmail(views.APIView):
    serializer_class = TeacherEmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = Teacher.objects.get(id=payload['user_id'])
            if not user.verify_status:
                user.verify_status = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
class TeacherLoginView(generics.GenericAPIView):
    serializer_class = TeacherLoginSerializer


    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TeacherPasswordResetView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        email = request.data['email']

        if Teacher.objects.filter(email=email).exists():
            user = Teacher.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Hi ' + user.first_name + ', Use the link below to reset your password \n'+ absurl
            data = {'email_body': email_body, 'email_subject': 'Reset your password', 'to_email': user.email}
            Util.send_email(data)
        else:
            return  Response({'Failure':'Error, Input a correct email'})

    

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
    
class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = TeacherSetNewPasswordSerializer
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Teacher.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message':                                                                                                                                                                                                                       'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
        
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = TeacherSetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
    
        
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = ('permissions.IsAuthenticated',)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def student_register(request):
    if request.method == 'POST':
        serializer = StudentRegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            student = serializer.save()
            data['response'] = 'successfully registered a new user'
            data['email'] = student.email
            data['first_name'] = student.first_name
            data['last_name'] = student.last_name
            data['phone_no'] = student.phone_no
            data['verify_status'] = student.verify_status

        else:
            data = serializer.errors
        return Response(data)

@csrf_exempt
def teacher_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        teacherData = Teacher.objects.get(email=email, password=password)
    except Teacher.DoesNotExist:
        teacherData = None
    if teacherData:
        if teacherData.verify_status == False:
            return JsonResponse({'status': 'failed', 'data': 'Please verify your email', 'message': 'Login failed', 'bool': False})
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
    except Teacher.DoesNotExist:
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
    
