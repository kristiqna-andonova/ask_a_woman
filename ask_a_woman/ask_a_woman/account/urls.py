from django.urls import path, include

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from ask_a_woman.account import views
from ask_a_woman.account.views import UserRegisterView




urlpatterns = [

    path('<int:pk>/', include([
        path('details/', views.profile_details, name='profile-details'),
        path('delete-profile/', views.DeleteUserProfile.as_view(), name='delete-profile')
    ])),

    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-profile/', views.UserProfileUpdateView.as_view(), name='update-profile'),
    path('change-password/', views.change_password, name='change-password'),

]

