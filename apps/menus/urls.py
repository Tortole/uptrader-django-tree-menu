"""
Module with menus app urls
"""

from django.urls import path
from .views import MainView, MenuItemView


urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("menu_item/<path:item_path>/", MenuItemView.as_view(), name="menu_item"),
]
