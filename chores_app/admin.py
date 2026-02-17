from django.contrib import admin

from .models import ChoreTask, TaskCompletionPhoto


class TaskCompletionPhotoInline(admin.TabularInline):
    model = TaskCompletionPhoto
    extra = 0


@admin.register(ChoreTask)
class ChoreTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'due_date', 'assigned_to')
    search_fields = ('title', 'description', 'assigned_to__username')
    inlines = [TaskCompletionPhotoInline]


@admin.register(TaskCompletionPhoto)
class TaskCompletionPhotoAdmin(admin.ModelAdmin):
    list_display = ('task', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('task__title', 'task__assigned_to__username')
