from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class post(models.Model):
    title =models.CharField(max_length=77)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # like=models.IntegerField(default=0)
    # dlike=models.IntegerField(default=0)

    def __str__(self):
        return '\'{}\' posted by {}'.format(self.title, self.author)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class comment(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=34, default=None)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    # active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return '{}: commented by {}'.format(self.post, self.name)