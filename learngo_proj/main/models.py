from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    verify_status = models.BooleanField(default=False)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)


    class Meta:
        verbose_name_plural = '1. Teachers'

    def __str__(self):
        return self.email
    
    def set_password(self, password):
        self.password = password
        self.save()
        return password
    
    def check_password(self, password):
        return self.password == password
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"
    

    
#probably not useful now
class CourseCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = '2. Course Categories'

    def __str__(self):
        return self.title


# Course model isn't being used yet, so we'll comment it out for now

class Course(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()    
    featured_image = models.ImageField(upload_to='course_images', null=True, blank=True)
    techstack = models.TextField(default='No techstack')

    class Meta:
        verbose_name_plural = '3. Courses'
    
    def __str__(self):
        return self.title

#probably not useful now
class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='chapter_videos', null=True)
    remarks = models.TextField(null = True)

    class Meta:
        verbose_name_plural = '4. Chapters'

    def __str__(self):
        return self.title


#    

class Student(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    verify_status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '5. Students'

    def __str__(self):
        return self.email
    
    def set_password(self, password):
        self.password = password
        self.save()
        return password    
    
    def completed_tasks(self):
        return self.Weeklytask_set.filter(student_status=True).count()
    
    def total_tasks(self):
        return self.Weeklytask_set.all().count()
    
    def pending_tasks(self):
        return self.Weeklytask_set.filter(student_status=False).count()


class Mentorship(models.Model):
    mentee = models.ForeignKey(Student, on_delete=models.CASCADE, null = True)
    Preferred_track = models.CharField(max_length=100, null = True)
    level = models.CharField(max_length=100, null = True)
    exist_knowledge = models.TextField(null = True)
    hours_per_week = models.CharField(max_length=100, null = True)
    twitter_link = models.URLField(unique=True, null = True)
    why_accept = models.TextField(null = True)
    feedback = models.TextField(null = True)


    class Meta:
        verbose_name_plural = '6. Mentorship'


class Weeklytask(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null= True )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=100)
    detail = models.TextField()
    # student_status = models.BooleanField(default=False, null=True)
    task_file = models.FileField(upload_to='weeklytask_files', null=True)
    submission_date = models.DateTimeField(null=True)
    submission_file = models.FileField(upload_to='weeklytask_files', null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = '7. Weeklytasks'


class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    notif_read_status = models.BooleanField(default=False, verbose_name='Notification Read Status')
    notif_created_time = models.DateTimeField(auto_now_add=True, verbose_name='Notification Created Time')
    notif_subject = models.CharField(max_length=100, verbose_name='Notification Subject')
    notif_text = models.TextField(verbose_name='Notification Text', null=True)


    class Meta:
        verbose_name_plural = '8. Notifications'

    def __str__(self):
        return self.notif_subject
    

    


    
    