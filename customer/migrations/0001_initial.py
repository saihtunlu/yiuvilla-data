# Generated by Django 3.1.1 on 2021-07-06 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.TextField(max_length=2000, null=True)),
                ('phone', models.TextField(blank=True, max_length=2000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]