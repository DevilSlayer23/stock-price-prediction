from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('script', views.Script.as_view(), name="script"),
    # path('predict', views.forecast, name="predict"),
    path('test', views.test, name="test"),
    path('main', views.main, name="main")
]