from django.contrib import admin
from .models import Instructions

class InstructionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Instructions, InstructionsAdmin)

