from rest_framework import serializers
from .models import Teacher, CourseCategory, Student, Course, Chapter, Weeklytask, Notification
from django.core.mail import send_mail
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only = True)

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'password2', 'phone_no']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        return Teacher.objects.create_user(**validated_data)

    def save(self):
        teacher = Teacher(
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            phone_no = self.validated_data['phone_no'],
            
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        teacher.set_password(password)
        teacher.save()
        return teacher
    
class TeacherLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)
    
    
    class Meta:
        model = Teacher
        fields = ['email', 'tokens', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        teacher = Teacher.objects.filter(email=email).first()

        teacher.last_login = timezone.now()
        teacher.save(update_fields=['last_login'])
        # import pdb; pdb.set_trace()

        if teacher is None:
            raise AuthenticationFailed('Credentials does not exist')

        if teacher.check_password(password):
            return {
            'email': teacher.email,
            'tokens': teacher.tokens()
        }
        if teacher.password!=password or not teacher:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        
        if not teacher.verify_status:
            raise AuthenticationFailed('Email is not verified')      
    

        return super().validate(attrs)
    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        model = Teacher
        fields = ['email']


class TeacherSetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 20, write_only = True)
    token = serializers.CharField(min_length = 1, write_only = True)
    uidb64 = serializers.CharField(min_length =1, write_only = True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = Teacher.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            
            user.set_password(password)           
        except Exception as e:
            raise AuthenticationFailed('The reset link is not valid', 401)
        return super().validate(attrs)
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
    

        
    
class StudentRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only = True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'password2', 'phone_no','verify_status']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        return Student.objects.create_user(**validated_data)

    def save(self):
        student = Student(
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            phone_no = self.validated_data['phone_no'],
            
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        student.set_password(password)
        student.save()
        return student
    
class TeacherEmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Teacher
        fields = ['token']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'phone_no', 'profile_picture','verify_status']


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title', 'description',]

# Course serializer will be used later

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'teacher', 'featured_image']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'course', 'title', 'description', 'video', 'remarks']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'password','phone_no', 'verify_status', 'profile_picture']

class StudentDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['pending_tasks', 'completed_tasks', 'total_tasks']

class WeeklytaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weeklytask
        fields = ['id', 'title', 'detail', 'add_time', 'update_time', 'submission_date', 'task_file', 'submission_file']

    def __init__(self, *args, **kwargs):
        super(WeeklytaskSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'student', 'teacher', 'notif_read_status', 'notif_subject', 'notif_text', 'notif_created_time']

            
