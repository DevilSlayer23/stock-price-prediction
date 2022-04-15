from django.shortcuts import render
from django.views.generic import View
import requests
import json
from django.http.response import JsonResponse
from pathlib import Path
from .lstm import predict



# # Create your views here.

def index(request):
    data = False
    while(not data):
        try:
            r = requests.get('https://live.nepse.repl.co/api.php')
            liveData = (r.json()["live_data"])
            json.dumps(liveData)
            

            context = {
                "liveData": liveData,
                }

            data = True
        except:
            data = False

    return render(request, 'main/index.html', context)


class Script(View):

    l = requests.get('https://live.nepse.repl.co/api.php').json()["live_data"]
    def get(self, request):
        selectedSymbol = self.l[0]['symbol']
        liveData = json.dumps(self.l)
        s = json.dumps(requests.get('https://www.sharesansar.com/company-chart/history?symbol='+selectedSymbol+'&resolution=1D&from=1607792736&to=1609305299').json())

        context = {
            "liveData": liveData,
            "symbol" : selectedSymbol,
            "script" : s,
        }
        return render(request,"main/script.html", context)



# # async def forecast(request):
#     data = await predict()

#     return render(request, "main/forecast.html", {'data' : data})
#     # return history


def test(request):
    data = predict()

    response = {
        'data' : data
    }

    return JsonResponse(response)


def main(request):
    return render(request, 'main/main.html')