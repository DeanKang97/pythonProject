# Generated by Django 3.1.6 on 2021-02-08 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256, null=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
