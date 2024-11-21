from django.urls import path

from ask_a_woman.common import views

urlpatterns = [
path('like/<int:pk>/', views.likes_functionality, name='like'),
    path('', views.HomeView.as_view(), name='home'),  # Home page: shows all posts

]