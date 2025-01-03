import nested_admin
from django.contrib import admin
from .models import Blog, BlogImage, Blog_Like, Blog_Comment, Category


class BlogImageInline(nested_admin.NestedStackedInline):
    """Inline for Blog images"""
    model = BlogImage
    extra = 1
    fields = ['image', 'image_url']
    readonly_fields = ['image_url']


class BlogLikeInline(nested_admin.NestedStackedInline):
    """Inline for Blog likes"""
    model = Blog_Like
    extra = 1
    fields = ['user']


class BlogCommentInline(nested_admin.NestedStackedInline):
    """Inline for Blog comments"""
    model = Blog_Comment
    extra = 1
    fields = ['user', 'content']


class BlogInline(nested_admin.NestedStackedInline):
    """Inline for Blogs under Categories"""
    model = Blog
    extra = 1
    fields = ['title', 'slug', 'excerpt', 'author', 'views']
    readonly_fields = ['slug']
    inlines = [BlogImageInline, BlogLikeInline, BlogCommentInline]


class CategoryAdmin(nested_admin.NestedModelAdmin):
    """Admin for Categories with nested blogs"""
    model = Category
    list_display = ['name']
    search_fields = ['name']
    inlines = [BlogInline]


# Register the admin
admin.site.register(Category, CategoryAdmin)
