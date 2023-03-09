from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.user_watchlist, name="user_watchlist"),
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("listing/<int:pk>", views.listing_detail, name="listing_detail"),
    path("bid/", views.place_bid, name="place_bid"),
    path("close_listing/", views.close_listing, name="close_listing"),
    path("closed_listing/", views.closed_listings, name="closed_listings"),
    path("add_comment/", views.add_comment, name="add_comment"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)