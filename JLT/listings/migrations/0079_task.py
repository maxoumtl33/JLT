# Generated by Django 5.0.3 on 2024-05-11 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0078_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')], max_length=20)),
            ],
        ),
    ]