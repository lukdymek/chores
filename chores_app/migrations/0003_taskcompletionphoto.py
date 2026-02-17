from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chores_app', '0002_create_initial_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCompletionPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='task_photos/%Y/%m/%d/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='chores_app.choretask')),
            ],
            options={
                'ordering': ['uploaded_at'],
            },
        ),
    ]
