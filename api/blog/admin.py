from django.contrib import admin
from .models import Category, Post, Comment
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE(attrs={"cols": 80, "rows": 20})},
    }

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
