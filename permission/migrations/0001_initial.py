# Generated by Django 3.1.1 on 2021-07-06 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.TextField(max_length=2000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.TextField(max_length=2000, null=True)),
                ('create', models.BooleanField(default=False)),
                ('read', models.BooleanField(default=False)),
                ('update', models.BooleanField(default=False)),
                ('delete', models.BooleanField(default=False)),
                ('edit_create', models.BooleanField(default=False)),
                ('edit_read', models.BooleanField(default=False)),
                ('edit_update', models.BooleanField(default=False)),
                ('edit_delete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.TextField(max_length=2000, null=True)),
                ('create', models.BooleanField(default=False)),
                ('read', models.BooleanField(default=False)),
                ('update', models.BooleanField(default=False)),
                ('delete', models.BooleanField(default=False)),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='permission.role')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
