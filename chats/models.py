from django.db import models
from django.contrib.auth.models import User
from main_app.models import consultation

# Create your models here.

class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    consultation_id = models.CharField(max_length=100)  # Cambiar a CharField
    sender = models.CharField(max_length=100)
    message = models.TextField()

    def __unicode__(self):
        return self.message


class Feedback(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __unicode__(self):
        return self.feedback