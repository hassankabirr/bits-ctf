# Generated by Django 4.0.2 on 2022-02-23 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_team_join_team_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='solved_questions',
            field=models.ManyToManyField(related_name='teams', to='main_app.Question'),
        ),
    ]
