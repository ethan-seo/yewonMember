# Generated by Django 2.2 on 2020-11-10 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yewonMemberApp', '0002_auto_20201108_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]