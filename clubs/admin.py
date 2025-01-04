from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coach, Dojo, Player
from accounts.admin import ProfileInline

# Register your models here.
class CoachAdmin(UserAdmin):
    list_display = ("email", "password", "certifications")

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('club info', {'fields': ('certifications',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'certifications'),
        }),
    )

    ordering = ('date_joined',)

    inlines = [ProfileInline]


class PlayerAdmin(UserAdmin):
    list_display = ("email", "password", "belt_rank")

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('club info', {'fields': ('belt_rank',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'belt_rank'),
        }),
    )

    inlines = [ProfileInline]

    ordering = ('date_joined',)

admin.site.register(Coach, CoachAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Dojo)