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
    parent = models.ForeignKey('self', related_name='children_set', on_delete=models.CASCADE, null=True, blank=True)
    hierarchy = models.CharField(max_length=255, null=True, blank=True)  # this field is required to create single query
                                                                          # in the DB, has the form el1:el2

    def children(self):
        """
        :return all children elements
        """
        return self.children_set.all()

    def parents_tree(self):
        if self.parent is not None:
            return [self.parent.id] + self.parent.parents_tree()
        else:
            return [None]


    def save(self, *args, **kwargs):
        tree = self.parents_tree()
        self.hierarchy = ':'.join([str(i) for i in tree if i])
        super(Item, self).save(*args, **kwargs)


    def __str__(self):
        return self.name
