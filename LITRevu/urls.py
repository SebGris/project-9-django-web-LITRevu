from django.conf import settings
from django.conf.urls.static import static
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
    path('posts/', review.views.create_ticket, name='posts'),
    path('ticket/<int:ticket_id>/edit', review.views.edit_ticket,
         name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete', review.views.delete_ticket,
         name='delete_ticket'),
    path('follow-users/', review.views.follow_users, name='follow_users'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
