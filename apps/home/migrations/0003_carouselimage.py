# Generated by Django 5.1.7 on 2025-05-05 07:12

import apps.home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_delete_carouselimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarouselImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="carousel_images/", validators=[]
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-uploaded_at"],
            },
        ),
    ]
