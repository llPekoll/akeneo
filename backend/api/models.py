from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Participant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

class Blacklist(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='blacklist')
    blocked_participant = models.ForeignKey(Participant, on_delete=models.CASCADE,related_name='blocked_by')

    class Meta:
        unique_together = ('participant', 'blocked_participant')

    def clean(self):
        if self.participant == self.blocked_participant:
            raise ValidationError("A participant cannot blacklist themselves.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.participant} blocks {self.blocked_participant}"

class Draw(models.Model):
    date = models.DateTimeField(auto_now_add=True)

class DrawResult(models.Model):
    draw = models.ForeignKey(Draw, on_delete=models.CASCADE, related_name='results')
    giver = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='given_gifts')
    receiver = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='received_gifts')
