from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('location/', views.location, name='location'),
    path('contact/', views.contact, name='contact'),
    path('post/<int:pk>/', views.detail, name='detail'),
    
    # Owner authentication
    path('owner/login/', views.owner_login, name='owner_login'),
    path('owner/logout/', views.owner_logout, name='owner_logout'),
    path('owner/dashboard/', views.dashboard, name='dashboard'),
    path('owner/create/', views.create_post, name='create_post'),
    path('owner/edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('owner/delete/<int:pk>/', views.delete_post, name='delete_post'),
]
