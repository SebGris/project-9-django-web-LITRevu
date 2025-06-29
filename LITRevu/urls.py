from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

import authentication.views
import review.views
from authentication.views import MyLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', MyLoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('reviews/', review.views.reviews, name='reviews'),
    path('flux/', review.views.flux, name='flux'),
    path('posts/', review.views.posts, name='posts'),
    path('ticket/create/', review.views.create_ticket, name='ticket-create'),
    path('ticket/<int:ticket_id>/edit/', review.views.edit_ticket,
         name='edit-ticket'),
    path('ticket/<int:ticket_id>/delete/', review.views.delete_ticket,
         name='delete-ticket'),
    path('review/create/', review.views.create_review, name='review-create'),
    path('review/<int:ticket_id>/create/', review.views.create_review,
         name='review-create-for-ticket'),
    path('review/<int:review_id>/edit/', review.views.edit_review,
         name='edit-review'),
    path('review/<int:review_id>/delete/', review.views.delete_review,
         name='delete-review'),
    path('follow-users/', review.views.follow_users, name='follow-users'),
    path('unfollow/<int:user_id>/', review.views.unfollow_user,
         name='unfollow-user'),
    path('stars-demo/', review.views.stars_demo, name='stars-demo'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
