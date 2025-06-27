from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)

    def __str__(self):
        message = f'{self.name}, {self.phone_number}, {self.email}, {self.subject}'
        return message
