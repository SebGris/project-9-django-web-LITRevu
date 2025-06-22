from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    title = models.CharField(max_length=128, default="Titre")
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    time_created = models.DateTimeField(default=timezone.now)

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

    class Meta:
        permissions = [
            ("change_own_ticket", "Peut modifier son propre ticket"),
        ]


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("change_own_review", "Peut modifier sa propre critique"),
        ]


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
