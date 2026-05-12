"""
Validation System — Business Logic
===================================
Pure functions that update ValidationItem state after each vote.
Import these from views; do not call model.save() anywhere else.
"""


def update_validation_result(item):
    """
    Recompute yes_votes, no_votes, total_votes, confidence_score and status
    for the given ValidationItem after a new vote has been cast.

    Decision rules (per spec):
      - Requires item.required_votes total votes for an automatic decision.
      - confidence_score = yes_percentage (0–100).
      - |yes% − no%| >= 30  →  accepted / rejected  (validated_by = "system")
      - |yes% − no%| <  30  →  needs_moderation      (validated_by = "none")
    """
    yes_votes = item.votes.filter(response="yes").count()
    no_votes = item.votes.filter(response="no").count()
    neutral_votes = item.votes.filter(response="neutral").count()
    total_votes = yes_votes + no_votes + neutral_votes

    item.yes_votes = yes_votes
    item.no_votes = no_votes
    item.neutral_votes = neutral_votes
    item.total_votes = total_votes

    if total_votes > 0:
        yes_percentage = (yes_votes / total_votes) * 100
        no_percentage = (no_votes / total_votes) * 100
    else:
        yes_percentage = 0.0
        no_percentage = 0.0

    item.confidence_score = yes_percentage

    if total_votes >= item.required_votes:
        difference = abs(yes_percentage - no_percentage)

        if difference >= 30:
            if yes_percentage > no_percentage:
                item.status = "accepted"
            else:
                item.status = "rejected"
            item.validated_by = "system"
        else:
            item.status = "needs_moderation"
            item.validated_by = "none"

    item.save()


def moderator_resolve_item(item, decision):
    """
    Allow a moderator to manually resolve a needs_moderation item.

    Arguments:
        item     — ValidationItem instance with status == "needs_moderation"
        decision — "accept" or "reject"

    Per spec: confidence_score is set to 80 and validated_by to "moderator".
    """
    if decision == "accept":
        item.status = "accepted"
    elif decision == "reject":
        item.status = "rejected"

    item.confidence_score = 80
    item.validated_by = "moderator"
    item.save()
