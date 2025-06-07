from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms, models


@login_required
def posts(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.uploader = request.user
            # now we can save
            ticket.save()
            return redirect('home')
    return render(request, 'review/posts.html', context={'form': form})


@login_required
def home(request):
    posts = models.Ticket.objects.all()
    return render(request, 'review/home.html', context={'posts': posts}, )
