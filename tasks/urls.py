from django.urls import path
from django.contrib import admin
from . import views

app_name = 'tasks'

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', views.home, name='home'),
]