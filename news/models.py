from django.db import models
from django.contrib.auth.models import User

class NewsCheck(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.time)

class NewsItem(models.Model):
    slug = models.CharField(unique=True, max_length=255)
    title = models.TextField()
    url = models.URLField()
    comment_url = models.URLField()
    created = models.DateTimeField()
    score = models.IntegerField()

    def __unicode__(self):
        return "%s" % self.title
