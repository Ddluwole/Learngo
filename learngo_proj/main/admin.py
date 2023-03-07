from django.contrib import admin
from .models import Teacher, CourseCategory, Student, Course, Chapter, Mentorship, Weeklytask, Notification

# Register your models here.
admin.site.register(Teacher)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Chapter)
admin.site.register(Mentorship)
admin.site.register(Weeklytask)

class Notificationadmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'teacher','notif_read_status', 'notif_subject']
admin.site.register(Notification, Notificationadmin)