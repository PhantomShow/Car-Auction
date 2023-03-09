from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from .forms import AuctionListingForm, BidForm

from .models import User, AuctionListing, Bid, ListingComment


def index(request):
    return render(request, "auctions/index.html", {
        'listings': AuctionListing.objects.filter(is_closed=False)
    })

def closed_listings(request):
    return render(request, "auctions/closed_listings.html", {
        'listings': AuctionListing.objects.filter(is_closed=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html", {'form':AuctionListingForm()})

def listing_detail(request, pk):
    try:
        listing = AuctionListing.objects.get(id=pk)
    except:
        raise Http404
    return render(request, "auctions/listing_detail.html", {'listing': listing, 'bid_form':BidForm()})

def user_watchlist(request):
    return render(request, "auctions/user_watchlist.html", {'watchlist': request.user.watchlist.all()})

@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        target_listing = AuctionListing.objects.get(id=request.POST['listing_id'])
        request.user.watchlist.add(target_listing)
        if request.POST['page'] == 'listing_detail':
            return render(request, "auctions/listing_detail.html", {'listing': target_listing})
        return HttpResponseRedirect(reverse(request.POST['page']))

@login_required
def remove_from_watchlist(request):
    if request.method == "POST":
        target_listing = AuctionListing.objects.get(id=request.POST['listing_id'])
        request.user.watchlist.remove(target_listing)
        if request.POST['page'] == 'listing_detail':
            return render(request, "auctions/listing_detail.html", {'listing': target_listing})
        return HttpResponseRedirect(reverse(request.POST['page']))


@login_required
def place_bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = request.user
            bid.listing = AuctionListing.objects.get(id=request.POST['listing_id'])
            if bid.perform_bid():
                bid.save()
                bid.listing.save()
                return HttpResponseRedirect(reverse('listing_detail', args=(bid.listing.id,)))
        
        return render(request, "auctions/listing_detail.html", {
            'listing': bid.listing, 
            'bid_form': BidForm(),
            'message': "Bid must be higher than current bid",
        })

@login_required
def add_comment(request):
    if request.method == "POST":
        comment_text = request.POST['comment']
        current_listing = AuctionListing.objects.get(id=request.POST['listing']) 
        new_comment = ListingComment(user=request.user, listing=current_listing, comment=comment_text)
        new_comment.save()
        return HttpResponseRedirect(reverse('listing_detail', args=(current_listing.id,)))

@login_required
def close_listing(request):
    if request.method == "POST":
        target_listing = AuctionListing.objects.get(id=request.POST['listing_id'])
        if target_listing.bids.count() > 0:
            target_listing.close()
            return HttpResponseRedirect(reverse('index'))

        return render(request, "auctions/listing_detail.html", {
            'listing': target_listing, 
            'message': "Cannot close without any bids.",
        })