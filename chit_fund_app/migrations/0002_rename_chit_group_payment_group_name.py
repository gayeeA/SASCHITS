# Generated by Django 5.1.1 on 2024-11-20 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chit_fund_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='chit_group',
            new_name='group_name',
        ),
    ]