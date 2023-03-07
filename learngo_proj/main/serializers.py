from rest_framework import serializers
from .models import Teacher, CourseCategory, Student, Course, Chapter, Weeklytask, Notification
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'email', 'password', 'phone_no', 'profile_picture', 'bio', 'skills',]

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
        fields = ['id', 'full_name', 'email', 'password', 'username', 'phone_no', 'bio']

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

            
