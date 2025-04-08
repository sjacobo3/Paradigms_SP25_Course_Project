from django.urls import path
from . import views

app_name = 'campusmart'

urlpatterns = [
    # /campusmart/index
    path('index/', views.index, name='index'),
    # /campusmart/register
    path('register/', views.register, name='register'),
    # /campusmart/login
    path('login/', views.login, name='login'),
    # /campusmart/logout
    path('logout/', views.logout, name='logout'),
    # /campusmart/dashboard
    path('dashboard/', views.dashboard, name='dashboard'), 
    # /campusmart/create
    path('create_listing/', views.create_listing, name='create_listing'),
    # /campusmart/update
    path('update_listing/', views.update_listing, name='update_listing'),
    # /campusmart/delete
    path('delete_listing/', views.delete_listing, name='delete_listing'),
]

    