from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Exists, OuterRef, Value
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models
from .forms import ReviewForm, TicketForm
from .models import UserFollows

User = get_user_model()


@login_required
def create_ticket(request):
    """
    Vue pour créer un nouveau ticket (demande de critique)
    """
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # Associer le ticket à l'utilisateur connecté
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Ticket créé avec succès !")
            return redirect('flux')
    return render(request, 'review/create_ticket.html', context={'form': form})


@login_required
def create_review(request, ticket_id=None):
    """
    Vue pour créer une critique.
    Si ticket_id est fourni : critique en réponse à un ticket existant
    Sinon : création d'un ticket + critique en une fois
    """
    if ticket_id:
        # Cas 1: Critique en réponse à un ticket existant
        ticket = get_object_or_404(models.Ticket, id=ticket_id)

        # Vérifier qu'aucune critique n'existe déjà pour ce ticket
        if ticket.reviews.exists():
            messages.error(
                request,
                "Une critique a déjà été publiée pour ce ticket."
            )
            return redirect('flux')

        # Déterminer si l'utilisateur est le créateur du ticket
        is_creator = (ticket.user == request.user)

        # Créer une classe de formulaire adaptée aux permissions :
        # - Si is_creator=True : formulaire complet (titre, description, image)
        # - Si is_creator=False : formulaire sans le champ image
        # Cette factory function retourne une CLASSE, pas une instance
        CustomTicketForm = forms.get_ticket_form(is_creator=is_creator)

        if request.method == 'POST':
            ticket_form = CustomTicketForm(
                request.POST,
                request.FILES,
                instance=ticket
            )
            # Désactiver les champs si l'utilisateur n'est pas le créateur
            if not is_creator:
                for field in ticket_form.fields.values():
                    field.disabled = True
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                # Sauvegarder la critique
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                messages.success(request, "Critique ajoutée avec succès !")
                return redirect('flux')
        else:
            # Affichage initial du formulaire
            ticket_form = CustomTicketForm(instance=ticket)
            review_form = ReviewForm()
        return render(request, 'review/create_review.html', {
            'ticket_form': ticket_form,
            'review_form': review_form,
            'ticket': ticket,
        })
    else:
        # Cas 2: Création ticket + critique en une fois
        if request.method == 'POST':
            ticket_form = TicketForm(request.POST, request.FILES)
            review_form = ReviewForm(request.POST)
            if ticket_form.is_valid() and review_form.is_valid():
                # Créer le ticket
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                # Créer la critique liée au ticket
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                messages.success(
                    request,
                    "Ticket et critique créés avec succès !"
                )
                return redirect('flux')
        else:
            # Affichage initial des formulaires vides
            ticket_form = TicketForm()
            review_form = ReviewForm()
        return render(request, 'review/create_review.html', {
            'ticket_form': ticket_form,
            'review_form': review_form,
        })


@login_required
def edit_ticket(request, ticket_id):
    """
    Vue pour modifier un ticket existant.
    Seul le propriétaire du ticket peut le modifier.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    # Vérifier que l'utilisateur est bien le propriétaire
    if ticket.user != request.user:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à modifier ce ticket."
        )
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_form = forms.TicketForm(
            request.POST,
            request.FILES,
            instance=ticket
        )
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Ticket modifié avec succès !")
            return redirect('posts')
    context = {
        'edit_form': edit_form,
    }
    return render(request, 'review/edit_ticket.html', context=context)


@login_required
def edit_review(request, review_id):
    """
    Vue pour modifier une critique existante.
    Seul l'auteur de la critique peut la modifier.
    """
    review = get_object_or_404(models.Review, id=review_id)
    # Vérifier que l'utilisateur est bien l'auteur
    if review.user != request.user:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à modifier cette critique."
        )
    edit_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        edit_form = forms.ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Critique modifiée avec succès !")
            return redirect('posts')
    context = {
        'edit_form': edit_form,
        'ticket': review.ticket,  # Afficher le ticket associé
    }
    return render(request, 'review/edit_review.html', context=context)


@login_required
def delete_ticket(request, ticket_id):
    """
    Vue pour supprimer un ticket.
    Seul le propriétaire peut supprimer son ticket.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    # Vérifier que l'utilisateur est bien l'auteur
    if ticket.user != request.user:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à supprimer ce ticket."
        )
    if request.method == 'POST':
        ticket.delete()  # Supprime aussi les critiques liées
        messages.success(request, "Ticket supprimé avec succès !")
        return redirect('posts')
    return render(request, 'review/delete_ticket.html')


@login_required
def delete_review(request, review_id):
    """
    Vue pour supprimer une critique.
    Seul l'auteur peut supprimer sa critique.
    """
    review = get_object_or_404(models.Review, id=review_id)
    # Vérifier que l'utilisateur est bien l'auteur
    if review.user != request.user:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à supprimer cette critique."
        )
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Critique supprimée avec succès !")
        return redirect('posts')
    return render(request, 'review/delete_review.html')

@login_required
def flux(request):
    """
    Vue principale du flux d'activité.
    Affiche les tickets et critiques des utilisateurs suivis.
    Inclut aussi les critiques sur les tickets de l'utilisateur connecté.
    """
    # Récupérer les utilisateurs suivis par l'utilisateur connecté
    followed_users = models.UserFollows.objects.filter(
        user=request.user
    ).values_list('followed_user', flat=True)

    # Liste des utilisateurs dont on veut voir le contenu (suivis + soi-même)
    users_to_show = list(followed_users) + [request.user.id]

    # Annoter les tickets pour savoir s'ils ont déjà une critique
    reviews_for_tickets = models.Review.objects.filter(ticket=OuterRef('pk'))
    tickets = models.Ticket.objects.filter(
        user__id__in=users_to_show
    ).annotate(
        post_type=Value('ticket', output_field=CharField()),  # c'est du texte
        has_review=Exists(reviews_for_tickets)  # Permet de masquer le bouton
    )

    # Récupérer les critiques des utilisateurs suivis + soi-même
    reviews = models.Review.objects.filter(
        user__id__in=users_to_show
    ).annotate(
        post_type=Value('review', output_field=CharField())
    )

    # Récupérer les tickets de l'utilisateur connecté
    user_tickets = models.Ticket.objects.filter(user=request.user)

    # Ajouter les critiques en réponse aux tickets de l'utilisateur connecté
    # (même si elles viennent d'utilisateurs non suivis)
    reviews_on_user_tickets = models.Review.objects.filter(
        ticket__in=user_tickets
    ).annotate(
        post_type=Value('review', output_field=CharField())
    )
    # Fusionner les deux QuerySets de critiques avec l'opérateur union (|)
    # Cela évite les doublons automatiquement
    reviews = reviews | reviews_on_user_tickets

    # Combiner et trier par date de création (plus récent en premier)
    flux = sorted(
        list(tickets) + list(reviews),
        key=lambda obj: obj.created,
        reverse=True
    )
    return render(request, 'review/flux.html', context={'flux': flux}, )


@login_required
def posts(request):
    """
    Vue de la page "Mes posts".
    Affiche tous les tickets et critiques créés par l'utilisateur connecté.
    """
    # Récupérer les tickets de l'utilisateur
    tickets = models.Ticket.objects.filter(user=request.user).annotate(
        post_type=Value('ticket', output_field=CharField())
    )
    # Récupérer les critiques de l'utilisateur
    reviews = models.Review.objects.filter(user=request.user).annotate(
        post_type=Value('review', output_field=CharField())
    )
    # Combiner et trier par date de création (plus récent en premier)
    posts = sorted(
        list(tickets) + list(reviews),
        key=lambda obj: getattr(obj, 'created', None),
        reverse=True
    )
    return render(request, 'review/posts.html', context={'posts': posts}, )

@login_required
def unfollow_user(request, user_id):
    """
    Vue pour se désabonner d'un utilisateur.
    Supprime le lien de suivi entre l'utilisateur connecté et
    l'utilisateur ciblé.
    """
    if request.method == "POST":
        follow = get_object_or_404(
            UserFollows,
            user=request.user,
            followed_user__id=user_id
        )
        follow.delete()
    return redirect('follow-users')

@login_required
def follow_users(request):
    """
    Vue de gestion des abonnements.
    Permet de suivre/ne plus suivre des utilisateurs et affiche
    la liste des abonnements et abonnés.
    """
    message = None
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, user=request.user)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user_to_follow = User.objects.get(username=username)
                # Vérifications de validité
                if user_to_follow == request.user:
                    message = "Vous ne pouvez pas vous suivre vous-même."
                elif models.UserFollows.objects.filter(
                    user=request.user,
                    followed_user=user_to_follow
                ).exists():
                    message = f"Vous suivez déjà {username}."
                else:
                    # Créer le lien de suivi
                    models.UserFollows.objects.create(
                        user=request.user,
                        followed_user=user_to_follow
                        )
                    message = f"Vous suivez maintenant {username}."
            except User.DoesNotExist:
                message = f"L'utilisateur '{username}' n'existe pas."
    else:
        form = forms.FollowUsersForm(user=request.user)

    # Récupérer les listes d'abonnés et d'abonnements
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


@login_required
def stars_demo(request):
    """Vue de démonstration pour tester l'affichage des étoiles"""
    reviews = models.Review.objects.select_related('user', 'ticket')[:5]
    return render(request, 'review/stars_demo.html', {
        'reviews': reviews
    })
