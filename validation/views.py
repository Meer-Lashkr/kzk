import json
import random

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import ValidationItem, ValidationVote
from .services import moderator_resolve_item, update_validation_result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_moderator(user):
    return user.is_authenticated and (
        getattr(user, "is_moderator", False)
        or user.is_staff
        or user.is_superuser
    )


def _next_item_for_user(user):
    """
    Return one random pending ValidationItem that this user has not yet voted on
    and that still needs more votes.
    Returns None if no such item exists.
    """
    already_voted = ValidationVote.objects.filter(user=user).values_list(
        "item_id", flat=True
    )
    candidates = ValidationItem.objects.filter(
        status="pending",
        total_votes__lt=F("required_votes"),
    ).exclude(
        id__in=already_voted,
    )

    count = candidates.count()
    if count == 0:
        return None
    return candidates[random.randint(0, count - 1)]


# ---------------------------------------------------------------------------
# 1. Validation home — landing / voting page
# ---------------------------------------------------------------------------

@login_required
def validation_home(request):
    """
    Main validation page. Fetches a pending item for the logged-in user
    and renders the voting interface.
    """
    item = _next_item_for_user(request.user)

    # Stats for the sidebar
    total_items = ValidationItem.objects.count()
    accepted = ValidationItem.objects.filter(status="accepted").count()
    rejected = ValidationItem.objects.filter(status="rejected").count()
    needs_mod = ValidationItem.objects.filter(status="needs_moderation").count()
    pending = ValidationItem.objects.filter(status="pending").count()
    user_votes = ValidationVote.objects.filter(user=request.user).count()

    context = {
        "item": item,
        "stats": {
            "total": total_items,
            "accepted": accepted,
            "rejected": rejected,
            "needs_moderation": needs_mod,
            "pending": pending,
            "user_votes": user_votes,
        },
    }
    return render(request, "validation/index.html", context)


# ---------------------------------------------------------------------------
# 2. Get next item (AJAX-friendly JSON endpoint)
# ---------------------------------------------------------------------------

@login_required
def validation_next(request):
    """
    GET /validation/next/
    Returns a JSON description of the next pending item for this user,
    or {"done": true} if the queue is empty.
    """
    item = _next_item_for_user(request.user)
    if item is None:
        return JsonResponse({"done": True})

    return JsonResponse({
        "done": False,
        "item": {
            "id": item.id,
            "data_type": item.data_type,
            "content": item.content,
            "yes_votes": item.yes_votes,
            "no_votes": item.no_votes,
            "total_votes": item.total_votes,
            "required_votes": item.required_votes,
            "confidence_score": round(item.confidence_score, 1),
        },
    })


# ---------------------------------------------------------------------------
# 3. Submit a vote
# ---------------------------------------------------------------------------

@login_required
@require_POST
def validation_submit(request):
    """
    POST /validation/submit/
    Body (JSON or form): item_id, response (yes|no)
    Returns JSON with updated counts and status.
    """
    # Accept both JSON body and regular form POST
    if request.content_type and "application/json" in request.content_type:
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({"error": "Invalid JSON."}, status=400)
    else:
        data = request.POST

    item_id = data.get("item_id")
    response = data.get("response", "").lower()

    if not item_id:
        return JsonResponse({"error": "item_id is required."}, status=400)
    if response not in ("yes", "no"):
        return JsonResponse({"error": "response must be 'yes' or 'no'."}, status=400)

    item = get_object_or_404(ValidationItem, pk=item_id)

    # Guard: item must still be pending and not yet full
    if item.status != "pending":
        return JsonResponse(
            {"error": "This item is no longer accepting votes."}, status=400
        )
    if item.total_votes >= item.required_votes:
        return JsonResponse(
            {"error": "This item has already reached its vote quota."}, status=400
        )
        

    # Guard: no duplicate votes
    if ValidationVote.objects.filter(item=item, user=request.user).exists():
        return JsonResponse(
            {"error": "You have already evaluated this item."}, status=400
        )

    # Create the vote and recalculate
    ValidationVote.objects.create(item=item, user=request.user, response=response)
    item.refresh_from_db()
    update_validation_result(item)
    item.refresh_from_db()

    return JsonResponse({
        "success": True,
        "item_id": item.id,
        "yes_votes": item.yes_votes,
        "no_votes": item.no_votes,
        "total_votes": item.total_votes,
        "confidence_score": round(item.confidence_score, 1),
        "status": item.status,
        "validated_by": item.validated_by,
    })


# ---------------------------------------------------------------------------
# 4. Moderator list
# ---------------------------------------------------------------------------

def moderation_list(request):
    """
    GET /validation/moderation/
    Only moderators and admins may access this view.
    Shows all items with status = needs_moderation.
    """
    if not _is_moderator(request.user):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You do not have permission to access this page.")

    items = ValidationItem.objects.filter(status="needs_moderation").order_by(
        "-updated_at"
    )
    context = {"items": items}
    return render(request, "validation/moderation.html", context)


# ---------------------------------------------------------------------------
# 5. Moderator resolve
# ---------------------------------------------------------------------------

@require_POST
def moderation_resolve(request, item_id):
    """
    POST /validation/moderation/<item_id>/resolve/
    Only moderators and admins may access this view.
    Body: decision = "accept" | "reject"
    """
    if not _is_moderator(request.user):
        return JsonResponse({"error": "Forbidden."}, status=403)

    item = get_object_or_404(ValidationItem, pk=item_id, status="needs_moderation")
    decision = request.POST.get("decision", "").lower()

    if decision not in ("accept", "reject"):
        return JsonResponse(
            {"error": "decision must be 'accept' or 'reject'."}, status=400
        )

    moderator_resolve_item(item, decision)

    # Redirect back to moderation list (works for both plain POST and AJAX).
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "item_id": item.id, "status": item.status})
    return redirect("moderation_list")
