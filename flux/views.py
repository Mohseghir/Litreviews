from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Value, CharField
from itertools import chain
from .models import Ticket, Review
from .forms import ReviewForm, TicketForm, DeleteTicketForm, DeleteReviewForm


@login_required(login_url='/')
def flux(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'flux/flux.html', {'posts': posts})


@login_required(login_url='/')
def posts(request):
    tickets = Ticket.objects.filter(user__exact=request.user)
    reviews = Review.objects.filter(user__exact=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'flux/posts.html', {'posts': posts})


@login_required(login_url='/')
def make_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            # messages.info(request, "Votre ticket vient d'être publié!")
            return redirect("flux")
    return render(request, "flux/create_ticket.html", context={"form": form})


@login_required(login_url='/')
def make_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            ticket.is_reviewed = True
            ticket.save()
            return redirect('flux')
    return render(request, 'flux/create_review.html', context={'form': form})


@login_required(login_url="/")
def make_review_ticket(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST, request.FILES)
        if any([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.is_reviewed = True
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("flux")
    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }
    return render(request, "flux/create_review_ticket.html",
                  context=context)
