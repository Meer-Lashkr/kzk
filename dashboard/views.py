from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datasets.models import CorrectionSubmission, ParallelTextSubmission, SentenceJudgmentSubmission
from forum.models import Question, Answer
from accounts.models import User, ActivityLog, AuditLog


def _require_role(request, *roles):
    """Return True and set error message if user lacks required role."""
    if not request.user.is_authenticated:
        return False
    return request.user.role in roles or request.user.is_superuser


@login_required
def dashboard_index(request):
    """Redirect to role-appropriate dashboard."""
    user = request.user
    if user.is_site_admin:
        return redirect('admin_dashboard')
    elif user.is_moderator:
        return redirect('moderator_dashboard')
    else:
        return redirect('user_dashboard')


@login_required
def user_dashboard(request):
    user = request.user
    context = {
        'my_questions': Question.objects.filter(author=user).order_by('-created_at')[:5],
        'my_answers': Answer.objects.filter(author=user).order_by('-created_at')[:5],
        'my_corrections': CorrectionSubmission.objects.filter(submitted_by=user).order_by('-created_at')[:5],
        'my_parallel_texts': ParallelTextSubmission.objects.filter(submitted_by=user).order_by('-created_at')[:5],
        'my_judgments': SentenceJudgmentSubmission.objects.filter(submitted_by=user).order_by('-created_at')[:5],
        'corrections_count': CorrectionSubmission.objects.filter(submitted_by=user).count(),
        'parallel_count': ParallelTextSubmission.objects.filter(submitted_by=user).count(),
        'judgments_count': SentenceJudgmentSubmission.objects.filter(submitted_by=user).count(),
        'questions_count': Question.objects.filter(author=user).count(),
        'answers_count': Answer.objects.filter(author=user).count(),
        'recent_activity': ActivityLog.objects.filter(user=user).order_by('-created_at')[:10],
    }
    return render(request, 'dashboard/user.html', context)


@login_required
def moderator_dashboard(request):
    if not request.user.is_moderator:
        messages.error(request, "Access denied.")
        return redirect('user_dashboard')

    context = {
        'recent_corrections': CorrectionSubmission.objects.order_by('-created_at')[:10],
        'recent_parallel': ParallelTextSubmission.objects.order_by('-created_at')[:10],
        'recent_judgments': SentenceJudgmentSubmission.objects.order_by('-created_at')[:10],
        'recent_questions': Question.objects.exclude(status='deleted_soft').order_by('-created_at')[:10],
        'recent_activity': ActivityLog.objects.order_by('-created_at')[:20],
        'total_corrections': CorrectionSubmission.objects.count(),
        'total_parallel': ParallelTextSubmission.objects.count(),
        'total_judgments': SentenceJudgmentSubmission.objects.count(),
    }
    return render(request, 'dashboard/moderator.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_site_admin:
        messages.error(request, "Access denied.")
        return redirect('user_dashboard')

    role_distribution = {
        'normal_user': User.objects.filter(role='normal_user').count(),
        'moderator': User.objects.filter(role='moderator').count(),
        'admin': User.objects.filter(role='admin').count(),
    }
    context = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'role_distribution': role_distribution,
        'total_questions': Question.objects.count(),
        'total_answers': Answer.objects.count(),
        'total_corrections': CorrectionSubmission.objects.count(),
        'total_parallel': ParallelTextSubmission.objects.count(),
        'total_judgments': SentenceJudgmentSubmission.objects.count(),
        'recent_users': User.objects.order_by('-date_joined')[:10],
        'audit_logs': AuditLog.objects.order_by('-created_at')[:20],
        'recent_activity': ActivityLog.objects.order_by('-created_at')[:20],
    }
    return render(request, 'dashboard/admin.html', context)
