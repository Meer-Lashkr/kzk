import csv
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.models import AuditLog
from datasets.models import CorrectionSubmission, ParallelTextSubmission, SentenceJudgmentSubmission


def is_admin_check(user):
    return user.is_authenticated and user.is_site_admin


def admin_required(view_func):
    """Simple decorator to require admin role."""
    from functools import wraps
    from django.shortcuts import redirect
    from django.contrib import messages

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_site_admin:
            messages.error(request, "Admin access required for data export.")
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def export_corrections_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="corrections.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'incorrect_text', 'corrected_text', 'language_variant', 'topic', 'notes',
                     'submitted_by', 'record_status', 'created_at'])
    for obj in CorrectionSubmission.objects.select_related('submitted_by').all():
        writer.writerow([
            obj.pk, obj.incorrect_text, obj.corrected_text, obj.language_variant,
            obj.topic or '', obj.notes or '',
            obj.submitted_by.username if obj.submitted_by else '',
            obj.record_status, obj.created_at.isoformat()
        ])
    return response


@login_required
@admin_required
def export_corrections_json(request):
    data = list(CorrectionSubmission.objects.select_related('submitted_by').values(
        'id', 'incorrect_text', 'corrected_text', 'language_variant', 'topic', 'notes',
        'submitted_by__username', 'record_status', 'created_at'
    ))
    return JsonResponse(data, safe=False)


@login_required
@admin_required
def export_parallel_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="parallel_texts.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'source_text', 'target_text', 'source_language', 'target_language',
                     'topic', 'notes', 'submitted_by', 'record_status', 'created_at'])
    for obj in ParallelTextSubmission.objects.select_related('submitted_by').all():
        writer.writerow([
            obj.pk, obj.source_text, obj.target_text, obj.source_language, obj.target_language,
            obj.topic or '', obj.notes or '',
            obj.submitted_by.username if obj.submitted_by else '',
            obj.record_status, obj.created_at.isoformat()
        ])
    return response


@login_required
@admin_required
def export_parallel_json(request):
    data = list(ParallelTextSubmission.objects.select_related('submitted_by').values(
        'id', 'source_text', 'target_text', 'source_language', 'target_language',
        'topic', 'notes', 'submitted_by__username', 'record_status', 'created_at'
    ))
    return JsonResponse(data, safe=False)


@login_required
@admin_required
def export_judgments_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sentence_judgments.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'sentence_text', 'binary_label', 'language_variant', 'topic', 'notes',
                     'submitted_by', 'record_status', 'created_at'])
    for obj in SentenceJudgmentSubmission.objects.select_related('submitted_by').all():
        writer.writerow([
            obj.pk, obj.sentence_text, obj.binary_label, obj.language_variant,
            obj.topic or '', obj.notes or '',
            obj.submitted_by.username if obj.submitted_by else '',
            obj.record_status, obj.created_at.isoformat()
        ])
    return response


@login_required
@admin_required
def export_judgments_json(request):
    data = list(SentenceJudgmentSubmission.objects.select_related('submitted_by').values(
        'id', 'sentence_text', 'binary_label', 'language_variant', 'topic', 'notes',
        'submitted_by__username', 'record_status', 'created_at'
    ))
    return JsonResponse(data, safe=False)
