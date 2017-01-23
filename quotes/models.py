from django.contrib.auth.models import Permission, User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='pic_folder/profile/', default = 'pic_folder/profile/None/no-img.png')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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


