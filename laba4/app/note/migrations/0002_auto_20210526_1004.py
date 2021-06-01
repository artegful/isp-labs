# Generated by Django 3.2.3 on 2021-05-26 07:04

import ckeditor_uploader.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("note", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="content",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name="note",
            name="create_time",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="note",
            name="update_time",
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
