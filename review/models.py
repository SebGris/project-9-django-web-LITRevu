from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def save(self, *args, **kwargs):
        if self.pk:
            old_ticket = Ticket.objects.filter(pk=self.pk).first()
            if (
                old_ticket and old_ticket.image and self.image
                and old_ticket.image != self.image
            ):
                old_ticket.image.delete(save=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # delete the image file when the ticket is deleted
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.headline} - {self.rating}/5 - {self.user.username}"

    # def get_stars_display(self):
    #     """Retourne l'affichage en étoiles du rating"""
    #     full_stars = "★" * self.rating
    #     empty_stars = "☆" * (5 - self.rating)
    #     return full_stars + empty_stars

    # def get_stars_html(self):
    #     """Retourne l'HTML pour afficher les étoiles"""
    #     stars_html = ""
    #     for i in range(1, 6):
    #         if i <= self.rating:
    #             stars_html += '<span class="star filled">★</span>'
    #         else:
    #             stars_html += '<span class="star empty">☆</span>'
    #     return stars_html


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='followed_by',
        on_delete=models.CASCADE
    )

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"
