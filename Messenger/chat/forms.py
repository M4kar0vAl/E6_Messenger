from django import forms

from .models import Chat, Message


class CreateChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name']
        labels = {
            'name': 'Chat name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
