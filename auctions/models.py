from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    watchlist = models.ManyToManyField(to='AuctionListing', default=[])

class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=24)
    seller = models.ForeignKey(to=User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    starting_bid = models.DecimalField(max_digits=11, decimal_places=2)
    # Need to add current_bid as a foreign key to make things easier.
    picture = models.ImageField(upload_to='auctions/static/auctions/images')
    description = models.TextField(max_length=128)
    is_closed = models.BooleanField(default=False)
    winner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, related_name='winner')
    sold_date = models.DateTimeField(null=True)

    def get_date(self):
        time = datetime.now()
        if self.create_date.day == time.day:
            return str(time.hour - self.create_date.hour) + " hours ago"
        else:
            if self.create_date.month == time.month:
                return str(time.day - self.create_date.day) + " days ago"
            else:
                if self.create_date.year == time.year:
                    return str(time.month - self.create_date.month) + " months ago"
        return self.create_date
    
    def price_formatted(self):
        return "${:,.2f}".format(self.price)

    def bid_formatted(self):
        return "${:,.2f}".format(self.starting_bid)

    def close(self):
        self.winner = Bid.objects.get(bid=self.starting_bid).user
        self.is_closed = True
        self.sold_date = datetime.now()
        self.save()
        return self.winner
    
    def get_winning_bid(self):
        return Bid.objects.get(bid=self.starting_bid).bid_formatted()

    def __str__(self) -> str:
        return self.title

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, null=True, related_name='bids')
    listing = models.ForeignKey(to='AuctionListing', on_delete=models.CASCADE, null=True, related_name='bids')
    bid = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    bid_date = models.DateTimeField(auto_now_add=True)

    def perform_bid(self):
        if self.bid > self.listing.starting_bid:
            self.listing.starting_bid = self.bid
            return True
        return False

    def bid_formatted(self):
        return "${:,.2f}".format(self.bid)
    
    def __str__(self) -> str:
        return f"{self.user} bid {self.bid} on {self.listing}"

class ListingComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(to='AuctionListing', on_delete=models.CASCADE, null=True, related_name='comments')
    comment = models.TextField(max_length=128, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
