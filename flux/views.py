from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Value, CharField
from itertools import chain
from .models import Ticket, Review
from .forms import ReviewForm, TicketForm, DeleteTicketForm, DeleteReviewForm
from django.contrib import messages


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
def create_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.info(request, "Votre ticket a été publié avec succes!")
            return redirect("flux")
    return render(request, "flux/create_ticket.html", context={"form": form})


@login_required(login_url='/')
def create_review(request, ticket_id):
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
def create_review_ticket(request):
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


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    delete_form = DeleteTicketForm()
    if request.method == "POST":
        if "edit_ticket" in request.POST:
            edit_form = TicketForm(request.POST, request.FILES,
                                   instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("posts")
        if "delete_ticket" in request.POST:
            delete_form = DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect("posts")
    context = {
        "edit_form": edit_form,
        "delete_form": delete_form,
    }
    return render(request, "flux/edit_ticket.html",
                  context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    edit_form = ReviewForm(instance=review)
    delete_form = DeleteReviewForm()
    if request.method == "POST":
        if "edit_review" in request.POST:
            edit_form = ReviewForm(request.POST,
                                   request.FILES,
                                   instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("posts")
        if "delete_review" in request.POST:
            print("Check")
            delete_form = DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect("posts")
    context = {
        "edit_form": edit_form,
        "delete_form": delete_form,
    }
    return render(request, "flux/edit_review.html",
                  context=context)
