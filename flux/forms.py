from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    """Ticket creation form."""
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    """Review creation form."""
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]

    CHOICES = [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    rating = forms.ChoiceField(label="Note", widget=forms.RadioSelect, choices=CHOICES)

