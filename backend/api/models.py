from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

class Blacklist(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='blacklist')
    blocked_participant = models.ForeignKey(Participant, on_delete=models.CASCADE,related_name='blocked_by')

class Draw(models.Model):
    date = models.DateTimeField(auto_now_add=True)

class DrawResult(models.Model):
    draw = models.ForeignKey(Draw, on_delete=models.CASCADE, related_name='results')
    giver = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='given_gifts')
    receiver = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='received_gifts')
