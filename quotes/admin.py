from django.contrib import admin
from .models import Category, Quotes, QuotesTags, Tags

# Register your models here.

admin.site.register(Category)
admin.site.register(Quotes)
admin.site.register(QuotesTags)
admin.site.register(Tags)
