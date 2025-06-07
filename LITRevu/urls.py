from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView)
from django.urls import path
import authentication.views
import review.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('home/', review.views.home, name='home'),
]
