# Generated by Django 3.0.6 on 2020-06-19 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_cardclass_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='status',
        ),
        migrations.RemoveField(
            model_name='status',
            name='cardClass',
        ),
    ]
