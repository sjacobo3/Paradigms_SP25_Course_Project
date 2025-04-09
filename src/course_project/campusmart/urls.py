from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
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
    # path('dashboard/', views.dashboard, name='dashboard'), 
    # /campusmart/create
    path('create_listing/', views.create_listing, name='create_listing'),

    # /campusmart/update
    path('update_listing/<int:listing_id>/', views.update_listing, name='update_listing'),

    # /campusmart/delete
    path('delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),

    # /campusmart/listings
    path('listings/', views.listing_all, name='listing_all'),
    
    # /campusmart/listings/pk
    path('listings/<int:pk>/', views.detail, name='detail'),

    # /campusmart/lstings/pk/message
    path('listings/<int:listing_id>/new_message/', views.conversation_new, name='conversation_new'),

    # /campusmart/inbox
    path('inbox/', views.inbox, name='inbox'),

    # /campusmart/inbox/conversation_id
    path('inbox/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    