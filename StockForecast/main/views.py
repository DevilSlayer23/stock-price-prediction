from django.shortcuts import render
import requests
import json
# Create your views here.
def index(request):
    data = False
    while(not data):
        try:
            r = requests.get('https://live.nepse.repl.co/api.php')
            liveData = (r.json()["live_data"])
            # print(liveData)
            

            context = {
                "liveData": liveData,
                }

            data = True
        except:
            data = False

    return render(request, 'main/index.html', context)


def script(request):
    if request.method == "POST":
        selectedSymbol = request.POST['symbol']
    data = False
    while(not data):
        try:
            l = requests.get('https://live.nepse.repl.co/api.php')
            liveData = (l.json()["live_data"])
            # print(liveData)
            h = requests.get(
                'https://www.sharesansar.com/company-chart/history?symbol=NABIL&resolution=1D&from=1607792736&to=1609305299')
            history = (h.json())
            json.dump(history)
            print(history)
            # print(liveData)

            context = {
                "history": history,
                "liveData": liveData,
                'symbol' : selectedSymbol
            }

            data = True
        except:
            data = False


    return render(request, 'main/script.html', context)
