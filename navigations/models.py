from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Menu'

    def __str__(self):
        return self.name


class Item(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    parents = models.ForeignKey('Item', related_name='children_set', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name
