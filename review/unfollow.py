from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import UserFollows

@login_required
def unfollow_user(request, user_id):
    if request.method == "POST":
        follow = get_object_or_404(UserFollows, user=request.user, followed_user__id=user_id)
        follow.delete()
    return redirect('follow_users')
