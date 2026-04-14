from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ActivityLog, AuditLog, PasswordResetToken
from .forms import ProfileEditForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('KZK Profile', {'fields': ('role', 'bio', 'profile_image')}),
    )


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'target_type', 'target_id', 'created_at')
    list_filter = ('action_type',)
    readonly_fields = ('created_at',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('performed_by', 'action_type', 'target_type', 'target_id', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'expires_at', 'used_at', 'created_at')
    readonly_fields = ('token', 'created_at')
