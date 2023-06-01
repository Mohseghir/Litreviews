from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Value, CharField, Q
from itertools import chain
from .models import Ticket, Review, UserFollows
from .forms import ReviewForm, TicketForm, DeleteTicketForm, DeleteReviewForm, FollowUsersForm
from django.contrib import messages
from authentication.models import User


@login_required(login_url='/')
def flux(request):
    # Récupération des utilisateurs suivis par l'utilisateur connecté
    user_following = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

    # Récupération des tickets liés aux utilisateurs suivis ou à l'utilisateur connecté
    tickets = Ticket.objects.filter(
        Q(user__in=user_following) | Q(user=request.user)
    )
    # Annotation du type de contenu pour les tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # Récupération des critiques liées aux utilisateurs suivis ou à l'utilisateur connecté
    reviews = Review.objects.filter(
        Q(user__in=user_following) | Q(user=request.user)
    )
    # Annotation du type de contenu pour les critiques
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    # Fusion des tickets et des critiques, triés par date de création décroissante
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    # Rendu du template avec les publications filtrées
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

    posts = list(posts)  # Convert the iterable to a list

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


@login_required
def follow_users(request):
    context = {}
    if request.method == "POST":
        form = FollowUsersForm(request.POST)
        if form.is_valid():
            follower = form.cleaned_data["follower"]
            try:
                user = User.objects.get(username__exact=follower)
            except User.DoesNotExist:
                user = None

            if user and user != request.user:  # Vérification si l'utilisateur n'est pas lui-même
                UserFollows.objects.create(user=request.user, followed_user=user)
                return redirect("follow_users")
            else:
                # Ajouter un message d'erreur indiquant que l'abonnement à soi-même n'est pas autorisé
                messages.error(request, "Vous ne pouvez pas vous abonner à vous-même.")
    else:
        form = FollowUsersForm()

    context["form"] = form
    context["following"] = UserFollows.objects.filter(user=request.user)
    context["followed_by"] = UserFollows.objects.filter(followed_user=request.user)
    return render(request, "flux/follow_users.html", context)


@login_required
def delete_follow(request, user_id):
    user = User.objects.get(id__exact=user_id)
    follow = UserFollows.objects.get(
        user__exact=request.user, followed_user__exact=user
    )
    if follow:
        follow.delete()
    return redirect("follow_users")
