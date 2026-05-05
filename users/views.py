from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .forms import CustomUserCreationForm, CustomUserLoginForm, \
    CustomUserUpdateForm
from main.models import Product


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main:index')
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required(login_url='/users/login')
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return HttpResponse(headers={'HX-Redirect': reverse('users:profile')})
            return redirect('users:profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    recommended_products = Product.objects.all().order_by('id')[:3]

    return TemplateResponse(request, 'users/profile.html', {
        'form': form,
        'user': request.user,
        'recommended_products': recommended_products,
    })


@login_required(login_url='/users/login')
def account_details(request):
    return TemplateResponse(request, 'users/partials/account_details.html', {'user': request.user})


@login_required(login_url='/users/login')
def edit_account_details(request):
    form = CustomUserUpdateForm(instance=request.user)
    return TemplateResponse(request, 'users/partials/edit_account_details.html', {
        'user': request.user,
        'form': form,
    })


@login_required(login_url='/users/login')
def update_account_details(request):
    
    if not request.headers.get('HX-Request') and request.method != 'POST':
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.clean()
            user.save()
            return TemplateResponse(request, 'users/partials/account_details.html', {'user': user})
        else:
            return TemplateResponse(request, 'users/partials/edit_account_details.html', {
                'user': request.user,
                'form': form,
            })
    
    return redirect('users:profile')


def logout_view(request):
    logout(request)
    if request.headers.get('HX-Request'):
        return HttpResponse(headers={'HX-Redirect': reverse('main:index')})
    return redirect('main:index')



