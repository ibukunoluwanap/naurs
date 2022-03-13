# Generated by Django 4.0.1 on 2022-03-11 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0017_delete_programenquirymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramEnquiryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=100, verbose_name='phone number')),
                ('enquiry', models.TextField(max_length=500, verbose_name='enquiry')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.programmodel', verbose_name='program')),
            ],
            options={
                'verbose_name': 'Program Enquiry',
                'verbose_name_plural': 'Program Enquiries',
            },
        ),
    ]