# Generated by Django 4.0.2 on 2022-03-08 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_lec_attendance'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Lec_Attendance',
            new_name='Lec_Stat',
        ),
    ]
