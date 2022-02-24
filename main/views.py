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

    l = requests.get('https://live.nepse.repl.co/api.php')
    liveData = (l.json()["live_data"])

    if request.method == "POST":
        selectedSymbol = request.POST['symbol']
        print(type(selectedSymbol))
    else:
        selectedSymbol = liveData[0]['symbol']
        print(selectedSymbol)


    context = {
        "liveData": liveData,
        'symbol' : selectedSymbol
    }

        

    return render(request, 'main/script.html', context)
