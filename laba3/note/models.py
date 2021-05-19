from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    def create(self):
        self.create_time = timezone.now()
        self.save()

    def __str__(self):
        return self.title