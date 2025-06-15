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
    path('reviews/', review.views.reviews, name='reviews'),
    path('ticket/create', review.views.create_ticket, name='ticket_create'),
    path('flux/', review.views.flux, name='flux'),
    path('posts/', review.views.posts, name='posts'),
    path('review/create', review.views.create_review, name='review_create'),
    path('review/<int:ticket_id>/create/', review.views.create_review, name='review_create_for_ticket'),
    path('ticket/<int:ticket_id>/edit', review.views.edit_ticket,
         name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete', review.views.delete_ticket,
         name='delete_ticket'),
    path('review/<int:review_id>/edit', review.views.edit_review,
         name='edit_review'),
    path('review/<int:review_id>/delete', review.views.delete_review,
         name='delete_review'),
    path('follow-users/', review.views.follow_users, name='follow_users'),
    path('unfollow/<int:user_id>/', review.views.unfollow_user, name='unfollow_user'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
