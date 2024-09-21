from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home,register, task_list, add_task, edit_task, delete_task, product_list, user_list  # Импортируйте нужные представления

urlpatterns = [
    path('', home, name='home'),
    path('task/', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('edit/<int:task_id>/', edit_task, name='edit_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('products/', product_list, name='product_list'),
    path('users/', user_list, name='user_list'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
