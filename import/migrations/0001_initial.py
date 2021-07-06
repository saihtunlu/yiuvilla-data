# Generated by Django 3.1.1 on 2021-07-06 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Imports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(default='', max_length=2000, null=True)),
                ('date', models.TextField(blank=True, max_length=2000, null=True)),
                ('total', models.TextField(default=0, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.TextField(default='0', max_length=2000, null=True)),
                ('number_of_fullfilled', models.TextField(default='0', max_length=2000, null=True)),
                ('primary_price', models.TextField(default='0', max_length=2000, null=True)),
                ('primary_price_yuan', models.TextField(default='0', max_length=2000, null=True)),
                ('sale_price', models.TextField(default='0', max_length=2000, null=True)),
                ('subtotal', models.TextField(default='0', max_length=2000, null=True)),
                ('margin', models.TextField(default='0', max_length=2000, null=True)),
                ('profit', models.TextField(default='0', max_length=2000, null=True)),
                ('name', models.TextField(blank=True, max_length=2000, null=True)),
                ('image', models.TextField(blank=True, max_length=2000, null=True)),
                ('link', models.TextField(blank=True, max_length=2000, null=True)),
                ('date', models.TextField(blank=True, max_length=2000, null=True)),
                ('imports', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='import.imports')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]