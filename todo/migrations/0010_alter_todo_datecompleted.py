# Generated by Django 4.0.1 on 2022-01-26 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_alter_todo_datecompleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='datecompleted',
            field=models.DateTimeField(null=True),
        ),
    ]