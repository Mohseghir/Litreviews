from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    AUTHOR = "AUTHOR"
    FOLLOWER = "FOLLOWER"

    ROLE_CHOICES = (
        (AUTHOR, "Auteur"),
        (FOLLOWER, "Abonné"),
    )
    profile_photo = models.ImageField(verbose_name="Image de profil")
    role = models.CharField(max_length=30,
                            choices=ROLE_CHOICES, verbose_name="Rôle")
