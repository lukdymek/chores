from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ChoreTask(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chore_tasks')
    due_date = models.DateField(default=timezone.localdate)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date', 'assigned_to__username', 'title']

    def __str__(self):
        return f'{self.title} ({self.assigned_to.username})'


class TaskCompletionPhoto(models.Model):
    task = models.ForeignKey(ChoreTask, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='task_photos/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f'Photo for {self.task.title} ({self.task.assigned_to.username})'
