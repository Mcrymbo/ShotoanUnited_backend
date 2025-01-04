from django.contrib import admin
from .models import News, Like, Comment, NewsImage, Category

# Register your models here.

class NewsImageInline(admin.StackedInline):
    """ inline admin for images """
    model = NewsImage
    extra = 1
    fields = ['image',]

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'content', 'date', 'views']
    search_fields = ['title', 'description']
    list_filter = ['date', 'author']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [NewsImageInline]


admin.site.register(News, NewsAdmin)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Category)
