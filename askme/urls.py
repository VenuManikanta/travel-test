from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = "askme"

urlpatterns = [
    # path('', views.Home.as_view(), name="askme_home"),
    # path('forms/', views.FormHome.as_view(), name="askme_form"),
    path('', views.ModelFormHome.as_view(), name="askme_mform"),
    path('chat/', views.Chat.as_view(), name="askme_chat"),
    path('recommend-food/', views.FoodRecommender.as_view(), name="askme_foodform"),
    path('lol/', views.AskAgain.as_view(), name="askme_again"),
    path('food/', views.FoodView.as_view(), name="askme_food"),
    path('trending/', views.MostSearched.as_view(), name="most_searched"),
    path('places/<str:place_name>/', views.PlaceView.as_view(), name="place_view"),
    path('places/<str:place_name>/<int:d>', views.PlaceDayView.as_view(), name="place_day_view"),
    path('my-itineraries/', views.ItinerariesView.as_view(), name="itineraries"),
    path('my-itineraries/<int:i_id>', views.SingleItineraryView.as_view(), name="single_itinerary"),
    path('flights/', views.flights, name="flights"),
    path('hotel/', views.hotel, name="hotel"),
]
 