
# Register your models here.
# admin.py
from django.contrib import admin
from .models import AboutPageContent
from .models import Course, Offer, Bundle

admin.site.register(AboutPageContent)


admin.site.register(Course)
admin.site.register(Offer)
admin.site.register(Bundle)