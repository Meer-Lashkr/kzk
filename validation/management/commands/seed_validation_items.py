"""
Management command: seed_validation_items
==========================================
Populates the ValidationItem queue from all existing dataset contributions.

Usage:
    python manage.py seed_validation_items

The command is idempotent — re-running it will skip records that already
have a corresponding ValidationItem (matched via source_type + source_id).
"""

from django.core.management.base import BaseCommand

from datasets.models import (
    CorrectionSubmission,
    ParallelTextSubmission,
    SentenceJudgmentSubmission,
)
from validation.models import ValidationItem


class Command(BaseCommand):
    help = "Seed ValidationItems from existing dataset contributions."

    def handle(self, *args, **options):
        created = 0
        skipped = 0

        # ── 1. Correction submissions ─────────────────────────────────────────
        for record in CorrectionSubmission.objects.all():
            source_type = "CorrectionSubmission"
            _, was_created = ValidationItem.objects.get_or_create(
                source_type=source_type,
                source_id=record.pk,
                defaults={
                    "data_type": "correction",
                    "content": {
                        "incorrect_sentence": record.incorrect_text,
                        "correct_sentence": record.corrected_text,
                        "language_variant": record.language_variant,
                        "topic": record.topic or "",
                    },
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        # ── 2. Parallel text submissions ──────────────────────────────────────
        for record in ParallelTextSubmission.objects.all():
            source_type = "ParallelTextSubmission"
            _, was_created = ValidationItem.objects.get_or_create(
                source_type=source_type,
                source_id=record.pk,
                defaults={
                    "data_type": "parallel_text",
                    "content": {
                        "source_language": record.source_language,
                        "target_language": record.target_language,
                        "source_text": record.source_text,
                        "target_text": record.target_text,
                    },
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        # ── 3. Sentence flagging (SentenceJudgmentSubmission) ─────────────────
        for record in SentenceJudgmentSubmission.objects.all():
            source_type = "SentenceJudgmentSubmission"
            _, was_created = ValidationItem.objects.get_or_create(
                source_type=source_type,
                source_id=record.pk,
                defaults={
                    "data_type": "flagged_data",
                    "content": {
                        "sentence": record.sentence_text,
                        "original_label": record.binary_label,
                        "language_variant": record.language_variant,
                    },
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created: {created} ValidationItem(s). "
                f"Skipped (already existed): {skipped}."
            )
        )
