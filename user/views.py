from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from .forms import CustomUserEditForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate , logout
from .forms import RegisterForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')  # Replace 'index' with the name of the view you want to redirect to after registration
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('index'))  # Replace 'home' with the name of your home view
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid username or password.')
    
    # If this is a GET request or the credentials were invalid, render the login page again.
    return render(request, 'login.html')

@login_required
def admin_dashboard(request):
    users = User.objects.all()
    if request.user.is_staff:
        if request.method == 'POST':
            if 'edit_user' in request.POST:
                user = get_object_or_404(User, pk=request.POST.get('user_id'))
                edit_form = CustomUserEditForm(request.POST, instance=user)
                if edit_form.is_valid():
                    edit_form.save()
                    messages.success(request, 'User updated successfully.')
                else:
                    messages.error(request, 'Error updating user.')
            elif 'delete_user' in request.POST:
                user = get_object_or_404(User, pk=request.POST.get('user_id'))
                user.delete()
                messages.success(request, 'User deleted successfully.')
            elif 'toggle_staff' in request.POST:
                user = get_object_or_404(User, pk=request.POST.get('user_id'))
                user.is_staff = not user.is_staff
                user.save()
                messages.success(request, 'User staff status changed.')
            return redirect('admin-dashboard')
        else:
            edit_form = CustomUserEditForm()
    
        return render(request, 'admin_dashboard.html', {
            'users': users,
            'edit_form': edit_form
        })
    else:
         return redirect('index')
    

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})