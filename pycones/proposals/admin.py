# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from pycones.proposals.actions import export_as_csv_action, send_confirmation_action, send_acceptance_action
from pycones.proposals.models import Proposal
from pycones.proposals.models import ProposalKind


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "speaker",
        "speaker_email",
        "kind",
        "audience_level",
        "language",
        "get_tag_list",
        "get_avg",
        'get_o0',
        'get_o1',
        "get_assigned_reviews",
        "get_completed_reviews",
        "notified",
        "accepted",
        "accepted_notified",
    ]
    list_filter = ["kind__name", "notified", "accepted"]
    actions = [
        export_as_csv_action("CSV Export", fields=[
            "id",
            "title",
            "speaker",
            "speaker_email",
            "kind",
            "audience_level",
            "language",
            "avg_property",
            "renormalization_o0_property",
            "renormalization_o1_property",
            "assigned_reviews_property",
            "completed_reviews_property",
            "tag_list_property"
        ]),
        send_confirmation_action("Sends confirmation email"),
        send_acceptance_action("Sends acceptance email")
    ]

    def get_avg(self, instance):
        return instance.avg()
    get_avg.short_description = _("Media")

    def get_completed_reviews(self, instance):
        return instance.completed_reviews_property
    get_completed_reviews.short_description = _("Revisiones completadas")

    def get_assigned_reviews(self, instance):
        return instance.assigned_reviews_property
    get_assigned_reviews.short_description = _("Revisiones asignadas")

    def get_tag_list(self, instance):
        return u", ".join(tag.name for tag in instance.tags.all())
    get_tag_list.short_description = _("Lista de etiquetas")

    def get_o0(self, instance):
        return instance.renormalization_o0()
    get_o0.short_description = _("O0")

    def get_o1(self, instance):
        return instance.renormalization_o1()
    get_o1.short_description = _("O1")


admin.site.register(ProposalKind)
