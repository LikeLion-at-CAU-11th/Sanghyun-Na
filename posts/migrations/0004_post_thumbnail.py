# Generated by Django 4.2.3 on 2023-08-01 10:35

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(), upload_to='post/thumbnail', verbose_name='썸네일'),
        ),
    ]