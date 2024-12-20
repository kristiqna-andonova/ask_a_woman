"""
URL configuration for ask_a_woman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ask_a_woman.common import views
from ask_a_woman.common.views import custom_404_view, custom_403_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ask_a_woman.common.urls')),
    path('account/', include('ask_a_woman.account.urls')),
    path('post/', include('ask_a_woman.post.urls')),
    path('search/', views.search_results, name='search-results'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = custom_404_view
handler403 = custom_403_view
