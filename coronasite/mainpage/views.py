from django.shortcuts import render
from .models import Update
import requests
# Create your views here.
def index(request):
    latest_bot_updates = Update.objects.order_by('-publication_date')[:3]
    coronavirus_information_begin = str(requests.get("https://www.worldometers.info/coronavirus/").content)
    coronavirus_information = coronavirus_information_begin[coronavirus_information_begin.find("<title>")+7:coronavirus_information_begin.find("</title>")].split()
    cases = coronavirus_information[3]
    deaths = coronavirus_information[6]
    recovered = coronavirus_information_begin[coronavirus_information_begin.find("<h1>Recovered:</h1>"):].split()[3]
    recovered_number = recovered[recovered.find("<span>")+6:recovered.find("</span>")]
    return render(request,"mainpage/mainpage.html",{'latest_bot_updates':latest_bot_updates,"cases":cases,"deaths":deaths,'recovered_number':recovered_number})
def contacts(request):
    return render(request,"mainpage/contacts.html")
