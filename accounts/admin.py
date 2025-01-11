from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Profile

# Register your models here.
class ProfileInline(admin.StackedInline):
    """ inline admin for images """
    model = Profile
    extra = 1
    fields = ['profile_pic', 'cover_photo', 'bio', 'phone_number']


class AccountAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Use email as the unique identifier
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    inlines = [ProfileInline]

admin.site.register(Account, AccountAdmin)
