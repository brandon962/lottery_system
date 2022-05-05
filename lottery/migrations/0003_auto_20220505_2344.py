# Generated by Django 3.2.13 on 2022-05-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0002_lottery_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='lottery_prize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize', models.CharField(max_length=10, verbose_name='prize level')),
            ],
            options={
                'verbose_name': 'prize level',
                'verbose_name_plural': 'prize level',
            },
        ),
        migrations.DeleteModel(
            name='lottery',
        ),
        migrations.RemoveField(
            model_name='lottery_table',
            name='urand',
        ),
        migrations.AlterField(
            model_name='lottery_table',
            name='uid',
            field=models.CharField(max_length=10, verbose_name='uid'),
        ),
    ]
