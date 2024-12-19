from django.contrib import admin
from .models import BlogPost

# Register the BlogPost model
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_private')
    list_filter = ('is_private', 'created_at')
    search_fields = ('title', 'content')
