from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import ActivityLog, AuditLog, PasswordResetToken

User = get_user_model()

class AccountsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com',
            role='normal_user'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword123',
            email='admin@example.com',
            role='admin'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'normal_user')
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)

    def test_superuser_creation(self):
        self.assertEqual(self.admin_user.role, 'admin')
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

    def test_activity_log(self):
        log = ActivityLog.objects.create(
            user=self.user,
            action_type='login'
        )
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action_type, 'login')

    def test_audit_log(self):
        log = AuditLog.objects.create(
            performed_by=self.admin_user,
            action_type='delete',
            target_type='user',
            target_id=str(self.user.pk)
        )
        self.assertEqual(log.performed_by, self.admin_user)
        self.assertEqual(log.action_type, 'delete')
