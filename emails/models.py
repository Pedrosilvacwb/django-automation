from ckeditor.fields import RichTextField
from django.db import models


class List(models.Model):
    email_list = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.email_list


class Subscriber(models.Model):
    email_address = models.EmailField(max_length=70)

    email_list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.email_address


class Email(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = RichTextField()
    attachment = models.FileField(upload_to="emai_attachments", blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.subject
