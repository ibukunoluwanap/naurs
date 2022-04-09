# Generated by Django 4.0.1 on 2022-04-09 09:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0005_programcalendar_alter_packagemodel_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProgramCalendar',
        ),
        migrations.AlterModelOptions(
            name='packagemodel',
            options={'verbose_name': 'Program', 'verbose_name_plural': 'Programs'},
        ),
        migrations.AlterModelOptions(
            name='programbenefitmodel',
            options={'verbose_name': 'Program Benefit', 'verbose_name_plural': 'Program Benefits'},
        ),
        migrations.AlterModelOptions(
            name='programenquirymodel',
            options={'verbose_name': 'Program Enquiry', 'verbose_name_plural': 'Program Enquiries'},
        ),
        migrations.AlterModelOptions(
            name='programmodel',
            options={'verbose_name': 'Program', 'verbose_name_plural': 'Programs'},
        ),
        migrations.AlterModelOptions(
            name='programpaymentmodel',
            options={'verbose_name': 'Program Payment', 'verbose_name_plural': 'Program Payments'},
        ),
        migrations.RemoveField(
            model_name='programmodel',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='programmodel',
            name='start_time',
        ),
        migrations.AddField(
            model_name='programmodel',
            name='calendar',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='calendar'),
            preserve_default=False,
        ),
    ]
