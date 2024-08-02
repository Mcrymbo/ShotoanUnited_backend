from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'role', 'is_active', 'is_admin', 'is_staff']
    search_fields = ('username', 'email')
    readonly_fields = ('id', 'date_joined', 'last_login', 'password')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)