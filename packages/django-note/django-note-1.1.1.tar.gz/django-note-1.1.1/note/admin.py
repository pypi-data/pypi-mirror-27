from django.contrib import admin
from.models import NotesList, Note


@admin.register(NotesList)
class TodoListAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    date_hierarchy = 'created'
    ordering = ('-modified',)


@admin.register(Note)
class TodoListItemAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_filter = ('done', )
