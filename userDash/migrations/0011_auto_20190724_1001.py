# Generated by Django 2.2.1 on 2019-07-24 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userDash', '0010_auto_20190724_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='health',
            field=models.CharField(default='F', max_length=7),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='swim',
            field=models.CharField(default='F', max_length=3),
        ),
    ]