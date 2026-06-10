from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings as django_settings
from .forms import RegistrationForm, ForgotPasswordForm, ResetPasswordForm, ProfileEditForm
from .models import User, PasswordResetToken
from accounts.models import ActivityLog
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'normal_user'
            user.is_active = False
            user.save()
            ActivityLog.objects.create(user=user, action_type='register')
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(f"/accounts/activate/{uid}/{token}/")
            
            send_mail(
                subject="Koma Zmanî Kurdî — Verify your email",
                message=f"Hello {user.username},\n\nPlease verify your email address to complete your registration by clicking the link below:\n{activation_link}\n\nIf you did not sign up for an account, please ignore this email.",
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            messages.success(request, "Registration successful! Please check your email to verify your account.")
            return redirect('check_email')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def check_email(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'registration/check_email.html')


def activate_account(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect('home')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your email has been verified. Welcome to Koma Zmanî Kurdî!")
        return redirect('home')
    else:
        messages.error(request, "The activation link was invalid or has expired.")
        return redirect('login')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'profile_user': request.user})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def settings_view(request):
    return render(request, 'accounts/settings.html')


@login_required
def change_password(request):
    """Allow logged-in users to change their password."""
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Keep user logged in after password change
            update_session_auth_hash(request, form.user)
            ActivityLog.objects.create(user=request.user, action_type='change_password')
            messages.success(request, "Your password has been changed successfully.")
            return redirect('settings')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Expire any existing tokens
                PasswordResetToken.objects.filter(user=user, used_at__isnull=True).update(
                    used_at=timezone.now()
                )
                token_obj = PasswordResetToken.objects.create(
                    user=user,
                    expires_at=timezone.now() + timedelta(hours=2)
                )
                reset_link = request.build_absolute_uri(
                    f"/accounts/reset-password/{token_obj.token}/"
                )
                send_mail(
                    subject="Koma Zmanî Kurdî — Password Reset",
                    message=f"Hello {user.username},\n\nClick the link below to reset your password:\n{reset_link}\n\nThis link expires in 2 hours.\n\nIf you did not request this, ignore this email.",
                    from_email=django_settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except User.DoesNotExist:
                pass  # Don't reveal whether the email exists
            messages.success(request, "If that email is registered, you will receive a reset link shortly.")
            return redirect('login')
    else:
        form = ForgotPasswordForm()
    return render(request, 'registration/forgot_password.html', {'form': form})


def reset_password(request, token):
    if request.user.is_authenticated:
        return redirect('home')
    token_obj = get_object_or_404(
        PasswordResetToken,
        token=token,
        used_at__isnull=True
    )
    if timezone.now() > token_obj.expires_at:
        messages.error(request, "This password reset link has expired. Please request a new one.")
        return redirect('forgot_password')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = token_obj.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            token_obj.used_at = timezone.now()
            token_obj.save()
            messages.success(request, "Your password has been reset. Please log in.")
            return redirect('login')
    else:
        form = ResetPasswordForm()
    return render(request, 'registration/reset_password.html', {'form': form, 'token': token})
