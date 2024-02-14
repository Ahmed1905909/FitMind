from django.shortcuts import render, redirect
from .forms import BlogPostForm , CourseForm
from .models import BlogPost , Course , Offer , Bundle
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import stripe


import os

# Create your views here.
def index(request):
    courses = Course.objects.all()[:3] 
    blogs = BlogPost.objects.all()[:3]
    context = {'username': request.user.username, 'courses': courses , 'blogs':blogs }
    return render(request, 'index.html', context)

# views.py

def about_page(request):
    about_file_path = os.path.join(os.path.dirname(__file__), 'about.txt')
    if request.method == 'POST' and request.user.is_staff:
        content = request.POST.get('content')
        with open(about_file_path, 'w') as file:
            file.write(content)
        return HttpResponse("Content updated successfully.")
    
    with open(about_file_path, 'r') as file:
        content = file.read()
    
    context = {
        'content': content,
        'is_staff': request.user.is_staff
    }
    return render(request, 'about.html', context)

@staff_member_required
def upload_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogPostForm()
    return render(request, 'upload_blog_post.html', {'form': form})

# def blog_posts(request):
#     posts = BlogPost.objects.all()
#     return render(request, 'blog_posts.html' , {'posts': posts})

def blog_posts(request):
    post_list = BlogPost.objects.all()
    paginator = Paginator(post_list, 6)  # Show 6 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog_posts.html', {'page_obj': page_obj})


@staff_member_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course-list')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

@staff_member_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'course': course})

@staff_member_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    return redirect('admin-dashboard')

def course_list(request):
    courses = Course.objects.all()
    bundles = Bundle.objects.all()
    return render(request, 'course_list.html', {'courses': courses , 'bundles': bundles})

@staff_member_required
def create_bundle(request):
    if request.method == 'POST':
        bundle_name = request.POST.get('bundle_name')
        bundle_price = request.POST.get('bundle_price')
        course_ids = request.POST.getlist('courses')
        courses = Course.objects.filter(id__in=course_ids)
        bundle = Bundle.objects.create(name=bundle_name, bundle_price=bundle_price)
        bundle.courses.set(courses)
        bundle.save()
        return redirect('admin-dashboard')
    else:
        courses = Course.objects.all()
        return render(request, 'create_course.html', {'courses': courses})
    


def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    context = {'course': course}
    return render(request, 'course_detail.html', context)

def create_payment_intent(request):
    course_id = request.POST.get('course_id')
    course = Course.objects.get(pk=course_id)

    stripe.api_key = stripe.test_secret_key  # Use live key for production

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(course.price * 100),  # Convert to cents
            currency='usd',
            description=course.title
        )
        return JsonResponse({'clientSecret': payment_intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failure(request):
    return render(request, 'payment_failure.html')