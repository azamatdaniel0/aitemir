from django.contrib import admin
from .models import Instructions, CustomUser

class InstructionsAdmin(admin.ModelAdmin):
    pass
class CustomUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(Instructions, InstructionsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

