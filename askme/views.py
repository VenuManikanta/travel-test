from django.shortcuts import render, get_list_or_404, redirect
from django.views import View
from .askAI import Ask, Clean_data, Clean_data2, AskChat, Clean_list, InteractChat, InteractChat2
from .forms import AskForm, QForm, FForm
from .models import Queries, Data, Food, Statistics, Search_history
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .helpers import find_closest_pair, generate_urls

from django.db.models import Sum, Count

import json
import requests
from datetime import datetime, timedelta
from urllib.request import urlopen

import time

# Create your views here.


class ModelFormHome(View):
    def get(self, request):
        form = QForm()
        ctx = {'form':form}
        return render(request, "askme/index.html", ctx)
    def post(self, request):
        try:
            form = QForm(request.POST)
            if not form.is_valid() :
                ctx = {'form' : form}
                return render(request, "askme/index.html", ctx)
            # If there are no errors, we would use it to get an answer
            place = request.POST.get("place")
            duration = request.POST.get("duration")

            stats_set = Statistics.objects.filter(stat_place=place.lower().strip(), stat_duration=duration)

            if stats_set:
                updated_values = {'stat_count': stats_set[0].stat_count+1}
            else:
                updated_values = {'stat_count': 1}

            obj, created = Statistics.objects.update_or_create(
                stat_place= place.lower().strip(), stat_duration=duration,
                defaults=updated_values
            )

            query_set = Data.objects.filter(gpt_place=place.lower().strip(), gpt_duration=duration)

            if query_set:
                
                time.sleep(5)

                heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
                page_link = ("http://127.0.0.1:8000/places/{}/{}".format(place,duration)).replace(" ","")
                if request.user.is_authenticated:
                    Search_history.objects.create(user=request.user, search_place=place,search_duration=duration,search_query="<h2><b>"+heading+"</b></h2>"+query_set[0].gpt_result)
                ctx = {"data":query_set[0].gpt_result, "place":place, "duration":duration, "heading":heading, "extra_button":'yes', 'page_link':page_link}
                return render(request, "askme/post_ans.html", ctx)
            
            else:
                test1 = "answer '0' if the place doesnt exist or '1' if it does: "+place
                test1_data = AskChat(test1)
                
                if "1" in test1_data:

                    
                    prompt = "hi"
                    data = AskChat(prompt)

                    p2 = "make a python list of all the places in the format:['place'] in the below text:"+data
                    data_p2 = AskChat(p2)
                    
                    # print(data_p2)
                    clean_data = Clean_list(data, data_p2)
                    heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
                    page_link = ("http://127.0.0.1:8000/places/{}/{}".format(place,duration)).replace(" ","")
                    ctx = {"data":clean_data, "place":place, "duration":duration, "heading":heading, "extra_button":'yes', 'page_link':page_link}

                    data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
                    data.save()

                    if request.user.is_authenticated:
                        Search_history.objects.create(user=request.user, search_place=place,search_duration=duration,search_query="<h2><b>"+heading+"</b></h2>"+clean_data)

                    # # add session data
                    # request.session["again_place"] = place
                    # request.session["again_duration"] = duration

                    return render(request, "askme/post_ans.html", ctx)
                else:
                    data = "I'm sorry, but '"+place+"' is not a known place or city. Can you provide more information or clarify the name of the destination you would like me to create an itinerary for?"
                    ctx = {"data":data}
                    return render(request, "askme/post_ans.html", ctx)
        except:
            data = "Something went wrong. Can you please try again."
            ctx = {"data":data}
            return render(request, "askme/error.html", ctx)

class AskAgain(View):
    def get(self, request):
        return redirect(reverse('askme:askme_mform'))
    def post(self, request):

        # print("in ASK AGAIN VIEW")

        place = request.POST.get("again_place")
        duration = request.POST.get("again_duration")
        
        # print(place)
        # print(duration)

        prompt = "hi"
        data = AskChat(prompt)

        p2 = "make a python list of all the places in the format:['place'] in the below text:"+data
        data_p2 = AskChat(p2)
                
        # print(data_p2)
        clean_data = Clean_list(data, data_p2)
        heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
        ctx = {"data":clean_data, "place":place, "duration":duration, "heading":heading, "extra_button":'yes'}

        # t = Data.objects.get(gpt_place= place, gpt_duration=duration)
        # t.gpt_result = clean_data  # change field
        # t.save()

        updated_values = {'gpt_result': clean_data}

        obj, created = Data.objects.update_or_create(
            gpt_place= place.lower().strip(), gpt_duration=duration,
            defaults=updated_values
        )

        # obj, created = Data.objects.get_or_create(gpt_place=place.lower().strip(), gpt_duration=duration, gpt_result=clean_data)
        # obj.save()

        # data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
        # data.save()

        return render(request, "askme/post_ans.html", ctx)

class FoodView(View):
    def post(self, request):
        place = request.POST.get("food_place")
        heading = "Food Recommendations for "+str(place).title()
        query_set = Food.objects.filter(gpt_place=place.lower().strip())

        if query_set:
            time.sleep(3.5)
            ctx = {"data":query_set[0].gpt_result, "place":place, "heading":heading}
            return render(request, "askme/post_ans.html", ctx)

        prompt = "hi"
        # print(prompt)

        data = AskChat(prompt)
        ctx = {"data":data, "place":place, "heading":heading}

        data = Food.objects.create(gpt_place= place.lower().strip(), gpt_result= data)
        data.save()

        # data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
        # data.save()

        return render(request, "askme/post_ans.html", ctx)


class MostSearched(View):
    def get(self, request):
        q = (Statistics.objects.values('stat_place').annotate(total = Sum('stat_count')))
        sorted_list = sorted(q, key=lambda x:x['total'], reverse=True)
        ctx = {'data':sorted_list[:3], 'heading':"Top 3 Most Searched Destinations"}
        return render(request, "askme/most_searched.html", ctx)

class PlaceView(View):
    def get(self, request, place_name):
        q = Data.objects.filter(gpt_place=place_name)
        ctx = {'data':q, 'heading':"Different Itineraries of "+place_name.title()}
        return render(request, "askme/place_view.html", ctx)

class PlaceDayView(View):
    def get(self, request, place_name, d):
        q = Data.objects.filter(gpt_place=place_name, gpt_duration=d)
        ctx = {'data':q[0].gpt_result, 'heading':str(d)+"-days Itinerary for "+place_name.title(), 'place':place_name, 'duration':d}
        return render(request, "askme/place_day_view.html", ctx)


class FoodRecommender(View):
    def get(self, request):
        form = FForm()
        ctx = {'form':form}
        return render(request, "askme/food_form.html", ctx)
    def post(self, request):
        
        place = request.POST.get("gpt_place")
        heading = "Food Recommendations for "+str(place).title()
        query_set = Food.objects.filter(gpt_place=place.lower().strip())

        if query_set:
            time.sleep(3.5)
            ctx = {"data":query_set[0].gpt_result, "place":place, "heading":heading}
            return render(request, "askme/post_food.html", ctx)

        prompt = "hi"
        # print(prompt)

        data = AskChat(prompt)
        ctx = {"data":data, "place":place, "heading":heading}

        data = Food.objects.create(gpt_place= place.lower().strip(), gpt_result= data)
        data.save()

        # data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
        # data.save()

        return render(request, "askme/post_food.html", ctx)


class Chat(View):
    def get(self, request):
        return redirect(reverse('askme:askme_mform'))
    def post(self, request):
        place = request.POST.get("again_place")
        duration = request.POST.get("again_duration")
        change_prompt = request.POST.get("personalize_prompt")
        
        t = Data.objects.get(gpt_place= place.lower().strip(), gpt_duration=duration)
        prev_prompt = t.gpt_result
        # print(place)
        # print(duration)

        
        data = InteractChat2(place, duration, user_inp=change_prompt)

        p2 = "make a python list of all the places in the format:['place'] in the below text:"+data
        data_p2 = AskChat(p2)
                
        # print(data_p2)
        clean_data = Clean_list(data, data_p2)
        heading = "Here's your "+str(duration)+"-days itinerary for "+str(place).title()
        heading2 = "Here's your "+str(duration)+"-days Personalized itinerary for "+str(place).title()
        
        
        if request.user.is_authenticated:
            latest_search = Search_history.objects.filter(user=request.user, search_place=place,search_duration=duration)[0]
            updated_values = {'search_query': "<h2><b>"+heading+"</b></h2>"+prev_prompt+"<h2><b>"+heading2+"</b></h2>"+clean_data}
            obj, created = Search_history.objects.update_or_create(
                    pk =latest_search.id, user=request.user, search_place=place,search_duration=duration,
                    defaults=updated_values
                )

        ctx = {"data":prev_prompt, "place":place, "duration":duration, "heading":heading, "extra_button":'yes', 'heading2':heading2, 'personalised':clean_data}

        # t = Data.objects.get(gpt_place= place, gpt_duration=duration)
        # t.gpt_result = clean_data  # change field
        # t.save()

        # updated_values = {'gpt_result': clean_data}

        # obj, created = Data.objects.update_or_create(
        #     gpt_place= place.lower().strip(), gpt_duration=duration,
        #     defaults=updated_values
        # )

        # obj, created = Data.objects.get_or_create(gpt_place=place.lower().strip(), gpt_duration=duration, gpt_result=clean_data)
        # obj.save()

        # data = Data.objects.create(gpt_place= place.lower().strip(), gpt_duration=duration, gpt_result= clean_data)
        # data.save()

        return render(request, "askme/post_ans.html", ctx)


class ItinerariesView(LoginRequiredMixin, View):
    def get(self, request):
        search_results = Search_history.objects.filter(user=request.user)
        ctx={'itineraries':search_results}
        return render(request, 'askme/itineraries.html',ctx)

class SingleItineraryView(LoginRequiredMixin, View):
    def get(self, request, i_id):
        search_results = Search_history.objects.get(pk=i_id)
        ctx={'itinerary':search_results}
        return render(request, 'askme/single_itinerary.html',ctx)


def flights(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    dest = request.POST.get('destination')
    (hotel,flight) = generate_urls(find_closest_pair(latitude,longitude)[0],dest.lower().strip())
    return redirect(flight)

def hotel(request):
    dest = request.POST.get('destination')
    today = datetime.today()
    today_date = str(today.year)+'-'+str(today.month)+'-'+str(today.day)
    tomorrow = today + timedelta(days=1)
    tomorrow_date = str(tomorrow.year)+'-'+str(tomorrow.month)+'-'+str(tomorrow.day)
    hotel = "https://www.expedia.co.in/Hotel-Search?destination={}&selected=&d1={}&startDate={}&d2={}&endDate={}&adults=2".format(str(dest), today_date, today_date, tomorrow_date, tomorrow_date)
    return redirect(hotel)