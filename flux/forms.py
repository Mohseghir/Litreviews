from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    CHOICES = [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowUsersForm(forms.Form):
    follower = forms.CharField(max_length=100)
