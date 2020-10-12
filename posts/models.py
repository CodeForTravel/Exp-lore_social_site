from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class ImagePost(models.Model):
    caption = models.TextField(max_length=4000)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True,on_delete="CASCADE")

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.caption

'''class VideoPost(models.Model):
    caption = models.TextField(max_length=4000)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True,on_delete="CASCADE")'''