# Generated by Django 5.1.7 on 2025-04-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_task_material'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='extra_materials',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
