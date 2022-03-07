# Generated by Django 4.0.2 on 2022-02-25 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_customuser_university'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='flag',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='main_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_body',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]