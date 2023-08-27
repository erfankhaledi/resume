from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('post/<slug>/', views.PostDetail.as_view(), name='post'),
    path('profile/', views.profile, name='profile'),

    path('create_post/', views.create_post, name="create_post"),
    path('update_post/<slug>/', views.LeadUpdateView.as_view(), name="update_post"),
    path('delete_post/<slug>/', views.delete_post, name="delete_post"),


]