# Generated by Django 4.1.1 on 2023-01-02 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_bids_listingcomments_auctionlisting"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionlisting",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
