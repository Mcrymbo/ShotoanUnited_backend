from django.contrib import admin
from .models import Event, EventImage

# Register your models here.
class EventImageInline(admin.StackedInline):
    """ inline admin for images """
    model = EventImage
    extra = 1
    field = ['image', 'image_url']
    readonly_fields = ['image_url']

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'content', 'date']
    search_fields = ['title', 'description']
    list_filter = ['date', 'title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventImageInline]


admin.site.register(Event, EventAdmin)
