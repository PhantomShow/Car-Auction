# Generated by Django 4.1.1 on 2023-01-03 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_alter_auctionlisting_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionlisting",
            name="description",
            field=models.TextField(
                default="1994 Mazda RX-7, 184,000 miles on chassis, 23,000 miles on new engine.",
                max_length=128,
            ),
            preserve_default=False,
        ),
    ]
