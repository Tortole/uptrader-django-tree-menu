"""
Module with models for tree menu
"""

from django.db import models


class Menu(models.Model):
    """
    Model for represent menu

    Fields:
        name - CharField - menu name
    """

    name = models.CharField(max_length=30)


class MenuItem(models.Model):
    """
    Model for represent menu item


    Fields:
        name - CharField - item name
        text - TextField - item text
        ancestor - ForeignKey(self) - link to item ancestor
        menu - ForeignKey(Menu) - menu to which current item is assigned
        url - CharField - item url

    NB:
        Item and his ancestor must be in same menu
    """

    name = models.CharField(max_length=30)
    text = models.TextField(max_length=300, blank=True)
    ancestor = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="descendants",
        blank=True,
        null=True,
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="items", blank=False
    )
    url = models.CharField(max_length=300, blank=True)

    def save(self, *args, **kwargs):
        if self.ancestor:
            assert (
                self.menu == self.ancestor.menu
            ), "Item and his ancestor must be in same menu"
        super(MenuItem, self).save(*args, **kwargs)
