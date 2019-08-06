from django.urls import path
from . import views 

app_name = 'elementryinfo'

urlpatterns = [
    path('',views.index,name='index')
]