from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


from .models import User,Listing, Bid, Watchlist, Comment


def index(request):
    return render(request, "auctions/index.html", {
                "username": request.user,
                "listings": Listing.objects.all()
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

@login_required
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
def newlisting(request):
    if request.method != "POST":
        return render(request, "auctions/createListing.html", {
                    "username": request.user,
                })
    elif request.method == "POST":
        if request.POST.get("imagename") is not None:
            imagename=request.POST.get("categoryname")+".png"
        else:
            imagename="noimage.png"
            listing = Listing(
            user=User.objects.get(username=request.POST.get("user")),
            title=request.POST.get("title"), 
            description=request.POST.get("description"), 
            startingprice=request.POST.get("startingprice"), 
            categoryname=request.POST.get("categoryname"),
            imagename=imagename)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def listing(request, listing_id):
    if request.user.is_authenticated:
        try:
            bids = Bid.objects.all().filter(listing=listing_id)
        except ObjectDoesNotExist:
            bids = None
    if request.user.is_authenticated:
        if request.method != "POST":
            listing = Listing.objects.get(pk=listing_id)
            user = User.objects.get(username=request.user)
            isOwner = False
            if listing.user.username == user.username:
                isOwner = True
            isactive = False
            try:
                watch = Watchlist.objects.get(user=user.pk, listing=listing_id)
                if watch is not None:
                    isactive = True
            except ObjectDoesNotExist:
                watch = None

            if bids is not None:
                offers=(bid.amount for bid in bids)
                maximum = max(offers, default=listing.startingprice)
            return render(request, "auctions/listingpage.html", {
                    "username": user.username,
                    "listing": listing,
                    "bids": bids,
                    "actualprice": maximum,
                    "isWatching": isactive,
                    "isOwner": isOwner

                })
        if request.method == "POST":
            if request.POST.get("status") is not None:
                if "Add" in request.POST.get("status"):
                    watchlist = Watchlist(
                    user=User.objects.get(username=request.user),
                    listing=Listing.objects.get(pk=listing_id))
                    watchlist.save()
                    return HttpResponseRedirect(reverse('listingpage', kwargs={'listing_id':listing_id}))
                else:
                    listing = Listing.objects.get(pk=listing_id)
                    user = User.objects.get(username=request.user)
                    try:
                        watchlist = Watchlist.objects.get(user=user.pk, listing=listing.id)
                        if watchlist is not None:
                            watchlist.delete()
                            return HttpResponseRedirect(reverse('listingpage', kwargs={'listing_id':listing_id}))
                    except ObjectDoesNotExist:
                        watch = None

                    return HttpResponseRedirect(reverse('listingpage', kwargs={'listing_id':listing_id}))
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def bidding(request, listing_id):
    if request.user.is_authenticated and request.method == "POST":
            newbid = Bid(
            user=User.objects.get(username=request.user),
            listing=Listing.objects.get(pk=listing_id),
            amount=request.POST.get("amount"))
            newbid.save()
            return HttpResponseRedirect(reverse('listingpage', kwargs={'listing_id':listing_id}))


@login_required
def watch(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            userWatchList = Watchlist.objects.all().filter(user=request.user)
            return render(request, "auctions/watchpage.html", {
                "watchlist": userWatchList
            })
        else:
            return HttpResponse("Operation not permitted.")
    else:
        return HttpResponseRedirect(reverse("login"))
    
@login_required
def closeListing(request, listing_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                listing=Listing.objects.filter(pk=listing_id).first()
                bids=Bid.objects.all().filter(listing=listing_id)
                if listing is not None:
                    listing.winner = max(bids, key=lambda bidder: bidder.amount).user.username
                    listing.save()
                return HttpResponseRedirect(reverse('listingpage', kwargs={'listing_id':listing_id}))
            except ObjectDoesNotExist:
                         return HttpResponse("Listing not found.")
    else:
        return HttpResponseRedirect(reverse("login"))
