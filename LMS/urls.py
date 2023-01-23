"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



admin.site.site_header = "LMS"
admin.site.site_title = "LMS admin panel"
admin.site.index_title = "Welcome to LMS admin panel"
admin.site.index_content = "Welcomesss to LMS admin panel"

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/books/', views.bookList.as_view()),
    path('api/books/<int:id>/', views.bookList.as_view()),
    path('api/books/search/', views.SearchbookList.as_view()),
    path('api/borrowed/', views.borrowList.as_view()),
    path('api/borrowed/<int:id>/', views.borrowList.as_view()),
    path('api/borrowed/search/', views.SearchborrowList.as_view()),
    path('api/category/', views.BookCatagoryList.as_view()),
    path('api/category/<int:id>/', views.BookCatagoryList.as_view()),
    path('api/register/', views.CustomUser.as_view()),
    path('api/register/<int:id>/', views.CustomUser.as_view()),
    path('api/register/<int:id>', views.CustomUser.as_view()),
    path('api/register/search/', views.searchCustomUser.as_view()),
    path('api/comment/', views.commentList.as_view()),
    path('api/comment/<int:id>', views.commentList.as_view()),
    path('api/login/', views.Login.as_view()),
    path('api/logout/', views.Logout.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)