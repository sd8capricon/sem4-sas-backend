# Generated by Django 4.0.2 on 2022-03-12 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_remove_attendance_date_lec_stat_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(default='test@email.com', max_length=30, unique=True),
            preserve_default=False,
        ),
    ]
