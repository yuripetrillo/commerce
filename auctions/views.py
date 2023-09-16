from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


from .models import User,Listing, Bid, Comment


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
            listing= Listing.objects.get(pk=listing_id)
            if bids is not None:
                offers=(bid.amount for bid in bids)
                maximum = max(offers, default=listing.startingprice)
            return render(request, "auctions/listingpage.html", {
                    "username": request.user,
                    "listing": listing,
                    "bids": bids,
                    "actualprice": maximum
                })
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
