from django.urls import path
from . import views

urlpatterns = [
    # Main validation landing / voting page
    path("", views.validation_home, name="validation_home"),

    # AJAX: fetch next pending item for this user
    path("next/", views.validation_next, name="validation_next"),

    # Submit a YES or NO vote
    path("submit/", views.validation_submit, name="validation_submit"),

    # Moderator: list all needs_moderation items
    path("moderation/", views.moderation_list, name="moderation_list"),

    # Moderator: resolve a single item
    path(
        "moderation/<int:item_id>/resolve/",
        views.moderation_resolve,
        name="moderation_resolve",
    ),
]
