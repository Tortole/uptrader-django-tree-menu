"""
Module with menus app views
"""

from django.views import View
from django.shortcuts import render

from .models import Menu


class MainView(View):
    """
    Render main page with all menus
    """

    template_name = "menus/main.html"

    def get(self, request):
        menus = [menu.name for menu in Menu.objects.all()]
        return render(request, self.template_name, context={"menus": menus})


class MenuItemView(View):
    """
    Render page with selected menu item by path
    """

    template_name = "menus/menu_item.html"

    def get(self, request, item_path):
        item_path_list = item_path.split("/")
        return render(
            request, self.template_name, context={"item_path": item_path_list}
        )
