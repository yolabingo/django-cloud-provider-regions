# Generated by Django 5.0.3 on 2024-03-27 21:16

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CloudProvider",
            fields=[
                (
                    "provider",
                    models.CharField(
                        max_length=4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(3)],
                    ),
                ),
            ],
            options={
                "verbose_name": "Cloud Provider",
            },
        ),
        migrations.CreateModel(
            name="CloudRegion",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "geographic_region",
                    models.CharField(
                        max_length=32,
                        validators=[django.core.validators.MinLengthValidator(2)],
                    ),
                ),
                (
                    "cardinality",
                    models.CharField(
                        max_length=12,
                        validators=[django.core.validators.MinLengthValidator(2)],
                    ),
                ),
                ("number", models.CharField(blank=True, default="", max_length=4)),
                ("original_region_name", models.CharField(max_length=64)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_cloud_provider_zones.cloudprovider",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cloud Region",
                "ordering": ["provider", "original_region_name"],
                "unique_together": {("provider", "original_region_name")},
            },
        ),
        migrations.CreateModel(
            name="CloudAvailabilityZone",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "az",
                    models.CharField(
                        max_length=4,
                        validators=[django.core.validators.MinLengthValidator(1)],
                    ),
                ),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_cloud_provider_zones.cloudregion",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cloud Availability Zone",
                "ordering": ["region", "az"],
                "unique_together": {("region", "az")},
            },
        ),
    ]
