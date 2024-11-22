from django.contrib import admin
from .models import News, Like, Comment, NewsImage

# Register your models here.

class NewsImageInline(admin.StackedInline):
    """ inline admin for images """
    model = NewsImage
    extra = 1
    field = ['image', 'image_url']
    readonly_fields = ['image_url']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'content', 'date', 'views']
    search_fields = ['title', 'description']
    list_filter = ['date', 'author']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [NewsImageInline]


admin.site.register(News, NewsAdmin)
admin.site.register(Like)
admin.site.register(Comment)
