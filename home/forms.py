from django import forms
from .models import Message


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'phone_number', 'message', 'subject', 'email', )
