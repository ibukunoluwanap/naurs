# Generated by Django 4.0.1 on 2022-04-07 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programbenefitmodel',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.programmodel', verbose_name='class'),
        ),
        migrations.AlterField(
            model_name='programenquirymodel',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.programmodel', verbose_name='class'),
        ),
        migrations.AlterField(
            model_name='programpaymentmodel',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.programmodel', verbose_name='class'),
        ),
        migrations.CreateModel(
            name='PackageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='title')),
                ('initial_price', models.PositiveIntegerField()),
                ('bonus_price', models.PositiveIntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('program', models.ManyToManyField(to='program.ProgramModel', verbose_name='class')),
            ],
            options={
                'verbose_name': 'Program',
                'verbose_name_plural': 'Programs',
            },
        ),
    ]
