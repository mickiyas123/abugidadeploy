# Generated by Django 4.0 on 2022-05-25 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='discussions.topic'),
        ),
    ]
