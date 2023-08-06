from django.contrib import admin
from .models import RsaKey


class RsaKeyAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "nbits"]
    search_fields = ["name", "title", "public_key", "private_key"]


admin.site.register(RsaKey, RsaKeyAdmin)
