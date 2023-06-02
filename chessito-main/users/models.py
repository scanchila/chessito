from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    win_ctd = models.IntegerField(default=0)
    onesignal_playerId = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.user.username} Profile'