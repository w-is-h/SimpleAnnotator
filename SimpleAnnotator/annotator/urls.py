from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', login_required(index), name='index'),
    path('annotate', login_required(annotate), name='annotate'),
    path('save', save, name='save'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
]
