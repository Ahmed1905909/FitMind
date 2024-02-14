from django.urls import path
from Main import views

urlpatterns = [
path('', views.index, name='index'),
path('about' , views.about_page , name= 'about'),
path('uplodblog' , views.upload_blog_post , name= 'upload_blog_post'),
path('Blog' , views.blog_posts , name= 'blog'),
path('create-course/', views.create_course, name='create-course'),
path('edit-course/<int:course_id>/', views.edit_course, name='edit-course'),
path('delete-course/<int:course_id>/', views.delete_course, name='delete-course'),
path('courses/', views.course_list, name='course-list'),
path('create-bundle/', views.create_bundle, name='create-bundle'),
]
