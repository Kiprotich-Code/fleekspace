from django.contrib import admin
from .models import Category, Post, Comment
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'body')
    actions = ['publish_posts', 'move_to_draft']
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE(attrs={"cols": 80, "rows": 20})},
    }

    def publish_posts(self, request, queryset):
        queryset.update(status='published')
    publish_posts.short_description = 'Mark selected posts as Published'

    def move_to_draft(self, request, queryset):
        queryset.update(status='draft')
    move_to_draft.short_description = 'Move selected posts to Draft'

    def save_model(self, request, obj, form, change):
        if '_publish' in request.POST:
            obj.status = 'published'
        elif '_draft' in request.POST:
            obj.status = 'draft'

    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form
    
    def response_change(self, request, obj):
        if "_publish" in request.POST:
            self.message_user(request, "Post published successfully!")
        elif "_draft" in request.POST:
            self.message_user(request, "Post saved as draft!")
        return super().response_change(request, obj)

    def render_change_form(self, request, context, *args, **kwargs):
        context["adminform"].form.fields["status"].widget.attrs["disabled"] = True
        return super().render_change_form(request, context, *args, **kwargs)
    

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
