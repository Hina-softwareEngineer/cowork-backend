# Generated by Django 4.2.16 on 2024-09-22 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coworkingspace', '0003_workspaceform_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspaceform',
            name='category',
            field=models.CharField(choices=[('coworking-space', 'Coworking Space'), ('corporate', 'Corporate')], default='corporate', max_length=100),
        ),
    ]
