from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ChoreTaskForm
from .models import ChoreTask, TaskCompletionPhoto


FAMILY_USERS = ['alex', 'olivia', 'olga', 'lukas']


def is_lukas_admin(user):
    return user.is_authenticated and user.username == 'lukas' and user.is_superuser


@login_required
def dashboard(request):
    selected_day = request.GET.get('day')
    try:
        today = date.fromisoformat(selected_day) if selected_day else timezone.localdate()
    except ValueError:
        today = timezone.localdate()
        messages.error(request, 'Invalid date format. Showing today instead.')

    users = []
    for username in FAMILY_USERS:
        user = User.objects.filter(username=username).first()
        if user:
            users.append(user)

    tasks_by_user = {}
    for user in users:
        tasks_by_user[user] = ChoreTask.objects.filter(assigned_to=user, due_date=today).prefetch_related('photos')

    return render(
        request,
        'dashboard.html',
        {
            'users': users,
            'tasks_by_user': tasks_by_user,
            'today': today,
            'is_lukas_admin': is_lukas_admin(request.user),
            'task_form': ChoreTaskForm(),
        },
    )


@login_required
@user_passes_test(is_lukas_admin)
def add_task(request):
    if request.method != 'POST':
        return redirect('dashboard')

    form = ChoreTaskForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Task added.')
    else:
        messages.error(request, 'Please fix the task form and try again.')

    return redirect('dashboard')


@login_required
def toggle_task(request, task_id):
    if request.method != 'POST':
        return redirect('dashboard')

    task = get_object_or_404(ChoreTask, id=task_id)
    if request.user != task.assigned_to and not is_lukas_admin(request.user):
        messages.error(request, 'You can only update your own chores.')
        return redirect('dashboard')

    task.is_completed = not task.is_completed
    task.completed_at = timezone.now() if task.is_completed else None
    task.save(update_fields=['is_completed', 'completed_at'])
    return redirect('dashboard')


@login_required
def upload_task_photos(request, task_id):
    if request.method != 'POST':
        return redirect('dashboard')

    task = get_object_or_404(ChoreTask, id=task_id)
    if request.user != task.assigned_to and not is_lukas_admin(request.user):
        messages.error(request, 'You can only upload photos for your own chores.')
        return redirect('dashboard')

    if not task.is_completed:
        messages.error(request, 'Mark the chore as done before uploading photos.')
        return redirect('dashboard')

    files = request.FILES.getlist('photos')
    if not files:
        single_file = request.FILES.get('photos')
        if single_file:
            files = [single_file]

    if not files:
        messages.error(request, 'No file was received. Please choose a photo and try again.')
        return redirect('dashboard')

    existing_count = task.photos.count()
    if existing_count + len(files) > 3:
        messages.error(request, 'Each task can have up to 3 photos in total.')
        return redirect('dashboard')

    for image_file in files:
        content_type = getattr(image_file, 'content_type', '') or ''
        if content_type and not content_type.startswith('image/'):
            messages.error(request, 'Only image files are allowed.')
            return redirect('dashboard')
        TaskCompletionPhoto.objects.create(task=task, image=image_file)

    messages.success(request, 'Photo upload complete.')
    return redirect('dashboard')
