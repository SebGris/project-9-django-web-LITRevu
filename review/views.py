from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from .models import UserFollows


from . import forms, models

User = get_user_model()


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Ticket créé avec succès !")
            return redirect('flux')
    return render(request, 'review/create_ticket.html', context={'form': form})


@login_required
def create_review(request, ticket_id=None):
    from .forms import TicketForm, ReviewForm
    if ticket_id:
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if request.method == 'POST':
            ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                messages.success(request, "Critique ajoutée avec succès !")
                return redirect('flux')
        else:
            ticket_form = TicketForm(instance=ticket)
            review_form = ReviewForm()
        return render(request, 'review/create_review.html', {
            'ticket_form': ticket_form,
            'review_form': review_form,
            'ticket': ticket,
        })
    else:
        if request.method == 'POST':
            ticket_form = TicketForm(request.POST, request.FILES)
            review_form = ReviewForm(request.POST)
            if ticket_form.is_valid() and review_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                messages.success(request, "Ticket et critique créés avec succès !")
                return redirect('flux')
        else:
            ticket_form = TicketForm()
            review_form = ReviewForm()
        return render(request, 'review/create_review.html', {
            'ticket_form': ticket_form,
            'review_form': review_form,
        })


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Ticket modifié avec succès !")
            return redirect('flux')
    context = {
        'edit_form': edit_form,
    }
    return render(request, 'review/edit_ticket.html', context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        edit_form = forms.ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Critique modifiée avec succès !")
            return redirect('flux')
    context = {
        'edit_form': edit_form,
    }
    return render(request, 'review/edit_review.html', context=context)


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Ticket supprimé avec succès !")
        return redirect('flux')
    return render(request, 'review/delete_ticket.html')


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Critique supprimée avec succès !")
        return redirect('flux')
    return render(request, 'review/delete_review.html')


@login_required
def reviews(request):
    reviews = models.Review.objects.all()
    return render(
        request,
        'review/reviews.html',
        context={'reviews': reviews},
    )


@login_required
def flux(request):
    # Récupérer les utilisateurs suivis
    followed_users = models.UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    users_to_show = list(followed_users) + [request.user.id]
    tickets = models.Ticket.objects.filter(user__id__in=users_to_show)
    reviews = models.Review.objects.filter(user__id__in=users_to_show)
    # Récupérer les tickets de l'utilisateur connecté
    user_tickets = models.Ticket.objects.filter(user=request.user)
    # Ajouter les reviews en réponse aux tickets de l'utilisateur connecté
    reviews_on_user_tickets = models.Review.objects.filter(ticket__in=user_tickets)
    reviews = reviews | reviews_on_user_tickets  # Utilisez union si reviews est un QuerySet
    # On ajoute un attribut post_type à chaque objet
    for t in tickets:   # annotate
        t.post_type = 'ticket'
    for r in reviews:
        r.post_type = 'review'
    flux = sorted(
        list(tickets) + list(reviews),
        key=lambda obj: obj.time_created,
        reverse=True
    )
    return render(request, 'review/flux.html', context={'flux': flux}, )


@login_required
def posts(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    # On ajoute un attribut post_type à chaque objet
    for t in tickets:
        t.post_type = 'ticket'
    for r in reviews:
        r.post_type = 'review'
    posts = sorted(
        list(tickets) + list(reviews),
        key=lambda obj: getattr(obj, 'time_created', None),
        reverse=True
    )
    return render(request, 'review/posts.html', context={'posts': posts}, )

@login_required
def unfollow_user(request, user_id):
    if request.method == "POST":
        follow = get_object_or_404(
            UserFollows,
            user=request.user,
            followed_user__id=user_id
        )
        follow.delete()
    return redirect('follow_users')

@login_required
def follow_users(request):
    message = None
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user_to_follow = User.objects.get(username=username)
                if user_to_follow == request.user:
                    message = "Vous ne pouvez pas vous suivre vous-même."
                elif models.UserFollows.objects.filter(
                    user=request.user,
                    followed_user=user_to_follow
                ).exists():
                    message = f"Vous suivez déjà {username}."
                else:
                    models.UserFollows.objects.create(
                        user=request.user,
                        followed_user=user_to_follow
                        )
                    message = f"Vous suivez maintenant {username}."
            except User.DoesNotExist:
                message = f"L'utilisateur '{username}' n'existe pas."
    else:
        form = forms.FollowUsersForm()
    followers = models.UserFollows.objects.filter(followed_user=request.user)
    following = models.UserFollows.objects.filter(user=request.user)
    return render(
        request,
        'review/follow_users_form.html',
        context={
            'form': form,
            'followers': followers,
            'following': following,
            'message': message
        }
    )
