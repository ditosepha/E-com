# Generated by Django 5.0.6 on 2024-06-14 10:07

import user.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', user.models.CustomUserManager()),
            ],
        ),
    ]
