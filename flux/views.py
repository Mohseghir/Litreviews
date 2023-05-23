from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Value, CharField
from itertools import chain
from .models import Ticket, Review


@login_required(login_url="/")
def flux(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, "flux/flux.html", {"posts": posts})


@login_required(login_url="/")
def posts(request):
    tickets = Ticket.objects.filter(user__exact=request.user)
    reviews = Review.objects.filter(user__exact=request.user)
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, "flux/posts.html", {"posts": posts})
