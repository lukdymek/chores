from django.contrib.auth.hashers import make_password
from django.db import migrations



def create_initial_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    defaults = {
        'alex': {'first_name': 'Alex', 'is_staff': False, 'is_superuser': False},
        'olivia': {'first_name': 'Olivia', 'is_staff': False, 'is_superuser': False},
        'olga': {'first_name': 'Olga', 'is_staff': False, 'is_superuser': False},
        'lukas': {'first_name': 'Lukas', 'is_staff': True, 'is_superuser': True},
    }

    for username, attrs in defaults.items():
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.password = make_password(username + '12345')
        user.first_name = attrs['first_name']
        user.is_staff = attrs['is_staff']
        user.is_superuser = attrs['is_superuser']
        user.is_active = True
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('chores_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_users, migrations.RunPython.noop),
    ]
