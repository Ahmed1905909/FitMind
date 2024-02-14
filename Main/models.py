# models.py
from django.db import models
from django.utils import timezone

class AboutPageContent(models.Model):
    content = models.TextField()

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='static/media', default='default_image.jpg')
    content = models.TextField()

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_price = models.DecimalField(max_digits=6, decimal_places=2)
    course_description = models.TextField()

    def __str__(self):
        return self.course_name

class Offer(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.course.course_name} - Offer"

class Bundle(models.Model):
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course)
    bundle_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
    

    