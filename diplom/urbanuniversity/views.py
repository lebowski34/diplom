from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Products
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm

User = get_user_model()

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        Task.objects.create(title=title)
        return redirect('task_list')
    return render(request, 'home.html')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.save()
        return redirect('task_list')
    return render(request, 'user_list.html', {'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

def product_list(request):
    products = Products.objects.all()
    return render(request, 'products/register.html', {'products': products})

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # перенаправление на страницу входа после регистрации
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def home(request):
    return render(request, 'home.html')