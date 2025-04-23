from django.contrib import admin
from accounts.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    list_filter = ('is_staff', 'is_active')
    list_per_page = 20


admin.site.register(User, UserAdmin)
