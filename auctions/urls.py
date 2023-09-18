from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("<int:listing_id>/listingpage", views.listing, name="listingpage"),
    path("<int:listing_id>/biddingpage", views.bidding, name="biddingpage"),
    path("watchpage", views.watch, name="watchpage"),
    path("<int:listing_id>/closeListing", views.closeListing, name="closeListing")

]
