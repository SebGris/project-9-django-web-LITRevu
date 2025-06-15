from itertools import chain

from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'review/create_ticket.html', context={'form': form})


@login_required
def create_review(request, ticket_id=None):
    from .forms import TicketForm, ReviewForm
    if ticket_id:
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if request.method == 'POST':
            ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
            review_form = ReviewForm(request.POST)
            if ticket_form.is_valid() and review_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                return redirect('home')
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
                return redirect('home')
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
        edit_form = forms.TicketForm(request.POST, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')
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
            return redirect('home')
    context = {
        'edit_form': edit_form,
    }
    return render(request, 'review/edit_review.html', context=context)


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')
    return render(request, 'review/delete_ticket.html')


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('home')
    return render(request, 'review/delete_review.html' )


@login_required
def home(request):
    posts = models.Ticket.objects.all()
    return render(request, 'review/home.html', context={'posts': posts}, )


@login_required
def reviews(request):
    reviews = models.Review.objects.all()
    return render(request, 'review/reviews.html', context={'reviews': reviews}, )


@login_required
def flux(request):
    flux = models.Ticket.objects.filter(user=request.user)
    return render(request, 'review/flux.html', context={'flux': flux}, )


@login_required
def posts(request):
    posts = models.Ticket.objects.filter(user=request.user)
    return render(request, 'review/posts.html', context={'posts': posts}, )


@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'review/follow_users_form.html',
                  context={'form': form})
