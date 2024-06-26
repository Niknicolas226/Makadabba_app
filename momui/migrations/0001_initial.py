# Generated by Django 4.2.6 on 2024-04-24 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('dietary_restrictions', models.CharField(blank=True, max_length=100)),
                ('cuisine_preferences', models.CharField(blank=True, max_length=100)),
                ('allergies', models.CharField(blank=True, max_length=100)),
                ('preferred_delivery_time', models.TimeField()),
                ('delivery_frequency', models.CharField(max_length=20)),
                ('people_served', models.IntegerField()),
                ('comments', models.TextField(blank=True)),
            ],
        ),
    ]
