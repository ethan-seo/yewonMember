# Generated by Django 2.2 on 2020-11-10 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yewonMemberApp', '0004_newsletter_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
