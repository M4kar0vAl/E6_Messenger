from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    chat = models.ForeignKey(to='Chat', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    GROUP = 'G'
    PERSONAL = 'P'
    TYPE_CHOICES = [
        (GROUP, 'Group'),
        (PERSONAL, 'Personal'),
    ]
    name = models.CharField(max_length=255, blank=True)
    participants = models.JSONField(default=dict)
    creator = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def get_absolute_url(self):
        return reverse_lazy('chat', args=[str(self.pk)])

    def add_participant(self, user):
        self.participants[user.pk] = ''
        self.save()

    def remove_participant(self, user):
        self.participants.pop(user.pk)
        self.save()
