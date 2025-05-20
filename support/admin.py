from django.contrib import admin
from .models import SupportTicket, SupportCategory

@admin.register(SupportCategory)
class SupportCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'category', 'status', 'created_at', 'answered_at']
    list_filter = ['status', 'category']
    search_fields = ['subject', 'message', 'user__username']
    readonly_fields = ['created_at', 'answered_at']
    fields = (
        'user',
        'category',
        'subject',
        'message',
        'image',
        'status',
        'answer',
        'answered_at',
        'created_at',
    )
