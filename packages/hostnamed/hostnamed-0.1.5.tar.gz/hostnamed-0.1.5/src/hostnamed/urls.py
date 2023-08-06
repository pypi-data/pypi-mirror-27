from django.urls import path
from . import views


urlpatterns = [
    path("update/", views.update, name="hostnamed.update"),
    path("query/", views.query, name="hostnamed.query"),
]
