# Generated by Django 4.1.1 on 2023-01-07 23:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0008_rename_bids_bid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="bid_date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="listingcomment",
            name="comment_date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
