# Generated by Django 4.0.2 on 2022-03-12 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_lec_stat_attendance_percentage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='date',
        ),
        migrations.AddField(
            model_name='lec_stat',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
