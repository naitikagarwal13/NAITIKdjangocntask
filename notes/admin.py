from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_pinned', 'created_at', 'updated_at']
    list_filter = ['is_pinned', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    list_editable = ['is_pinned']
    ordering = ['-is_pinned', '-updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Note Information', {
            'fields': ('title', 'content', 'is_pinned')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
