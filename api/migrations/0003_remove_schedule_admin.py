# Generated by Django 5.0.6 on 2024-06-22 20:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_alter_route_destination_station_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="schedule",
            name="admin",
        ),
    ]