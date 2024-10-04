"""
Module with tag for draw menu
"""

from django import template
from django.db.models import Q
from django.forms.models import model_to_dict

from typing import List

from ..models import MenuItem


register = template.Library()


def create_menu(items, selected_item_id):
    """
    Create menu from list of MenuItem

    Param:
        items - List[MenuItem] - menu item list
        selected_item_id - int - id of selected item
    """

    menu = {}
    items_links = {}

    for item in items:
        item_id = str(item.id)

        # If item's descendant has passed cycle before
        if item_id in items_links:
            items_links[item_id] = dict(items_links[item_id], **model_to_dict(item))
        else:
            items_links[item_id] = model_to_dict(item)
            items_links[item_id]["descendants"] = {}

        # If item selected
        if selected_item_id and (item_id == selected_item_id):
            items_links[item_id]["selected"] = True

        # If item has an ancestor
        if item.ancestor:
            item_ancestor_id = str(item.ancestor.id)
            # If item's ancestor has passed cycle before
            if item_ancestor_id in items_links:
                # then add link to current item in ancestor dictionary
                items_links[item_ancestor_id]["descendants"][item_id] = items_links[
                    item_id
                ]
            else:
                # else create
                items_links[item_ancestor_id] = {
                    "descendants": {item_id: items_links[item_id]},
                }
        else:
            # Add root item in menu
            menu[item_id] = items_links[item_id]

    return menu


@register.inclusion_tag("menus/draw_menu.html")
def draw_menu(menu_name: str = None, selected_item_path: List[str] = None):
    """
    Draw menu by name or by menu item path

    Param:
        menu_name - str - name of the menu to be drawn
        selected_item_path - List[str] - list path to selected item

    NB:
        Only one of menu_name or selected_item_path must be defined
    """

    assert (menu_name is not None) ^ (
        selected_item_path is not None
    ), "Only one of menu_name or selected_item_path must be defined"

    selected_item_id = None

    if selected_item_path:
        # Get menu items either in selected_item_path or with ancestor in selected_item_path
        items = MenuItem.objects.filter(
            Q(id__in=selected_item_path) | Q(ancestor__in=selected_item_path)
        ).order_by("id")

        selected_item_id = selected_item_path[-1]
    else:
        # Get menu items from menu
        items = MenuItem.objects.filter(menu__name=menu_name).order_by("id")

    menu = create_menu(items, selected_item_id)

    return {"menu": menu}
