from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.
from django.utils import timezone


class Category(models.Model):
    cat_name = models.CharField(max_length=250)

    def __str__(self):
        return self.cat_name


class Tags(models.Model):
    tag_name = models.CharField(max_length=250)

    def __str__(self):
        return self.tag_name


class Quotes(models.Model):
    user = models.ForeignKey(User)
    quote_text = models.TextField()
    category_name = models.ForeignKey(Category)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.quote_text


class QuotesTags(models.Model):
    quote_id = models.ForeignKey(Quotes)
    tags = models.ForeignKey(Tags)

    def __str__(self):
        return self.quote_id.quote_text + '-' + self.tags.tag_name


