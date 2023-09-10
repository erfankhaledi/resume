from django.db import models
from django.shortcuts import reverse


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='images', default="placeholder...")
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, null=True)
    slug = models.SlugField()
    link = models.URLField(null=True, blank=True)  # Added link field

    
    def get_absolute_url(self):
        return reverse("base:post", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.headline
    