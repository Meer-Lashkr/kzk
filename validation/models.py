from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ValidationItem(models.Model):
    """
    A single piece of Kurdish linguistic data submitted for community validation.
    Wraps one of the three contribution types: correction, parallel_text, flagged_data.
    """

    DATA_TYPE_CHOICES = [
        ("correction", "Correction"),
        ("parallel_text", "Parallel Text"),
        ("flagged_data", "Flagged Data"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("needs_moderation", "Needs Moderation"),
    ]

    VALIDATED_BY_CHOICES = [
        ("system", "System"),
        ("moderator", "Moderator"),
        ("none", "None"),
    ]

    data_type = models.CharField(max_length=30, choices=DATA_TYPE_CHOICES)

    # JSON blob containing the displayable content for the item.
    # Format depends on data_type — see services.py for details.
    content = models.JSONField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending",
    )

    yes_votes = models.PositiveIntegerField(default=0)
    no_votes = models.PositiveIntegerField(default=0)
    neutral_votes = models.PositiveIntegerField(default=0)
    total_votes = models.PositiveIntegerField(default=0)

    # Percentage (0–100) of users who voted YES.
    confidence_score = models.FloatField(default=0.0)

    # Number of votes required before an automatic decision is made.
    required_votes = models.PositiveIntegerField(default=6)

    validated_by = models.CharField(
        max_length=30,
        choices=VALIDATED_BY_CHOICES,
        default="none",
    )

    # Back-reference to the original dataset record (used by the seed command
    # to avoid creating duplicate ValidationItems on re-runs).
    source_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Model name of the originating dataset record.",
    )
    source_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="PK of the originating dataset record.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        # Prevent duplicate ValidationItems for the same source record.
        unique_together = [("source_type", "source_id")]

    def __str__(self):
        return f"ValidationItem #{self.pk} [{self.data_type}] — {self.status}"

    @property
    def yes_percentage(self):
        if self.total_votes == 0:
            return 0.0
        return (self.yes_votes / self.total_votes) * 100

    @property
    def no_percentage(self):
        if self.total_votes == 0:
            return 0.0
        return (self.no_votes / self.total_votes) * 100


class ValidationVote(models.Model):
    """
    Records a single user's YES/NO evaluation of a ValidationItem.
    Each user may only vote once per item (enforced by unique_together).
    """

    RESPONSE_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
        ("neutral", "Neutral"),
    ]

    item = models.ForeignKey(
        ValidationItem,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="validation_votes",
    )
    response = models.CharField(max_length=10, choices=RESPONSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("item", "user")]

    def __str__(self):
        return f"{self.user} → {self.response} on ValidationItem #{self.item_id}"
