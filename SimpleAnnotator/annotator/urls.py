from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('annotate', annotate, name='annotate'),
    path('save', save, name='save'),
]
