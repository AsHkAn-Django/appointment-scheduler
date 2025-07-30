from django.contrib import admin
from .models import Appointment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import CustomUser
from users.forms import CustomUserCreationForm, CustomUserChangeForm



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'hour', 'minute', 'details']
    ordering = ['date']
    list_filter = ['user', 'date',  'hour', 'minute']
    search_fields = ['user', 'details']


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ("email", "full_name", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name",)}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2"),
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
