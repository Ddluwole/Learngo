from django.db import models

# Create your models here.
class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    skills = models.TextField(default='No skills')


    class Meta:
        verbose_name_plural = '1. Teachers'

    def __str__(self):
        return self.full_name

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
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    interested_category = models.ManyToManyField(CourseCategory)

    class Meta:
        verbose_name_plural = '5. Students'