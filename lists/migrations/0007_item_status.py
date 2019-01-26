# Generated by Django 2.1.5 on 2019-01-26 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_list_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('SCH', 'Scheduled'), ('INP', 'In progress'), ('COM', 'Completed')], default='SCH', max_length=3),
        ),
    ]