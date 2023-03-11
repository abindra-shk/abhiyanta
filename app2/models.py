from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=10)

class notes(models.Model):
    title= models.CharField(max_length=100)
    author= models.CharField(max_length=100)
    pdf =models.FileField(upload_to='notes/pdfs/')

def __str__(self):
    return self.titile

      