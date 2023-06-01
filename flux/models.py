# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from PIL import Image
from django.core.exceptions import ValidationError


class Ticket(models.Model):
    """model pour un ticket"""
    IMAGE_MAX_SIZE = (250, 250)

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    objects = models.Manager()  # Ajout du gestionnaire d'objets par défaut

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()


class Review(models.Model):
    """model pour une revue"""
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()  # Ajout du gestionnaire d'objets par défaut


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )
    objects = models.Manager()  # Ajout du gestionnaire d'objets par défaut

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        )

    def clean(self):
        if self.user == self.followed_user:
            raise ValidationError("Un utilisateur ne peut pas s'abonner à lui-même.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
