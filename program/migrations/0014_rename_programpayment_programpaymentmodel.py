# Generated by Django 4.0.1 on 2022-03-08 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0013_alter_programpayment_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProgramPayment',
            new_name='ProgramPaymentModel',
        ),
    ]