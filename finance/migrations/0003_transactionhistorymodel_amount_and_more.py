# Generated by Django 4.0.1 on 2022-05-28 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_transactionhistorymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistorymodel',
            name='amount',
            field=models.FloatField(default=100, verbose_name='Amount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='amount',
            field=models.FloatField(verbose_name='Amount'),
        ),
    ]