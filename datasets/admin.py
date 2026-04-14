from django.contrib import admin
from .models import CorrectionSubmission, ParallelTextSubmission, SentenceJudgmentSubmission


@admin.register(CorrectionSubmission)
class CorrectionSubmissionAdmin(admin.ModelAdmin):
    list_display = ('submitted_by', 'language_variant', 'record_status', 'created_at')
    list_filter = ('language_variant', 'record_status')
    search_fields = ('incorrect_text', 'corrected_text')


@admin.register(ParallelTextSubmission)
class ParallelTextSubmissionAdmin(admin.ModelAdmin):
    list_display = ('submitted_by', 'source_language', 'target_language', 'record_status', 'created_at')
    list_filter = ('source_language', 'target_language', 'record_status')


@admin.register(SentenceJudgmentSubmission)
class SentenceJudgmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('submitted_by', 'binary_label', 'language_variant', 'record_status', 'created_at')
    list_filter = ('binary_label', 'language_variant', 'record_status')
