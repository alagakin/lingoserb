from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser


class AdminUser(UserAdmin):
    list_display = ['username', 'lang']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('picture', 'lang')}),
    )


admin.site.register(CustomUser, AdminUser)
