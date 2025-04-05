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
    path('logout/', views.logout, name='logout')
    
]

    