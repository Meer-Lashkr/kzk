from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    ROLE_CHOICES = (
        ('normal_user', 'Normal User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal_user')
    bio = models.TextField(blank=True, null=True, help_text="Short bio about the contributor")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)


    @property
    def is_moderator(self):
        return self.role in ['moderator', 'admin'] or self.is_staff or self.is_superuser

    @property
    def is_site_admin(self):
        return self.role == 'admin' or self.is_superuser

    def __str__(self):
        return self.username


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ResetToken for {self.user.username}"


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activity_logs')
    action_type = models.CharField(max_length=100)
    target_type = models.CharField(max_length=100, blank=True, null=True)
    target_id = models.IntegerField(null=True, blank=True)
    metadata_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} — {self.action_type}"


class AuditLog(models.Model):
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action_type = models.CharField(max_length=100)
    target_type = models.CharField(max_length=100, blank=True, null=True)
    target_id = models.IntegerField(null=True, blank=True)
    before_json = models.JSONField(default=dict, blank=True)
    after_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.performed_by} — {self.action_type} on {self.target_type} #{self.target_id}"
