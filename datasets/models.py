from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

RECORD_STATUS = (
    ('active', 'Active'),
    ('under_review', 'Under Review'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('deleted_soft', 'Deleted'),
)

LANGUAGE_VARIANT_CHOICES = (
    ('sorani', 'Sorani'),
    ('kurmanji', 'Kurmanji'),
    ('hawrami', 'Hawrami'),
    ('zazaki', 'Zazaki'),
    ('unknown', 'Unknown / Mixed'),
)

BINARY_LABEL_CHOICES = (
    ('correct', 'Correct'),
    ('incorrect', 'Incorrect'),
)


class CorrectionSubmission(models.Model):
    """Incorrect → Correct sentence pair submissions."""
    incorrect_text = models.TextField(help_text="The incorrect/original sentence")
    corrected_text = models.TextField(help_text="The corrected version of the sentence")
    language_variant = models.CharField(max_length=20, choices=LANGUAGE_VARIANT_CHOICES, default='sorani')
    topic = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True, help_text="Optional explanation of the correction")
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='correction_submissions')
    record_status = models.CharField(max_length=20, choices=RECORD_STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Correction by {self.submitted_by}: {self.incorrect_text[:40]}"


class ParallelTextSubmission(models.Model):
    """Bilingual or bidialectal aligned text submissions."""
    source_text = models.TextField()
    target_text = models.TextField()
    source_language = models.CharField(max_length=50, default='Sorani Kurdish')
    target_language = models.CharField(max_length=50, default='English')
    topic = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='parallel_text_submissions')
    record_status = models.CharField(max_length=20, choices=RECORD_STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Parallel ({self.source_language} → {self.target_language}) by {self.submitted_by}"


class SentenceJudgmentSubmission(models.Model):
    """Sentence Flagging — binary yes/no judgment about sentence grammatical correctness."""
    sentence_text = models.TextField()
    binary_label = models.CharField(max_length=10, choices=BINARY_LABEL_CHOICES)
    language_variant = models.CharField(max_length=20, choices=LANGUAGE_VARIANT_CHOICES, default='sorani')
    topic = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='judgment_submissions')
    record_status = models.CharField(max_length=20, choices=RECORD_STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Sentence Flagging'
        verbose_name_plural = 'Sentence Flaggings'

    def __str__(self):
        return f"Flagging ({self.binary_label}) by {self.submitted_by}: {self.sentence_text[:40]}"

