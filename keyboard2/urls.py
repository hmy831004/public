from django.urls import path
from . import views

urlpatterns = [
	path('',views.keyboard,name='keyboard'),
]

