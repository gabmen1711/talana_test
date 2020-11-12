from django.contrib import admin
from .models import *


class ParticipantsAdminView(admin.ModelAdmin):
    fields = ["name", "last_name", "email", "subscribed_on"]
    search_fields = ["name", "last_name", "email"]
    list_filter = ["email"]


class WinnersAdminView(admin.ModelAdmin):
    fields = ["participant_id"]


admin.site.register(Participants, ParticipantsAdminView)
admin.site.register(Winners, WinnersAdminView)
