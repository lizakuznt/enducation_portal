# Generated by Django 5.1.7 on 2025-04-14 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_completedtask_file_path_completedtask_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='material',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.educationalmaterial'),
        ),
    ]
