from django.contrib import admin
from vault.models import PasswordEntry

class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'encrypted_data', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    list_filter = ('user',)
    list_per_page = 20

admin.register(PasswordEntry, PasswordEntryAdmin)