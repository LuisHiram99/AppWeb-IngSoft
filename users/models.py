from django.db import models
from PIL import Image
from django.template.defaulttags import comment
from django.conf import settings

#quite el user
class Profile(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    image= models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.first_name

