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
    parents = models.ForeignKey('self', related_name='children_set', on_delete=models.CASCADE, null=True, blank=True)
    # hierarchy = models.ManyToManyField('self', null=True, blank=True, auto_created=True)
    hierarchy = models.CharField(max_length=255, null=True, blank=True)

    def children(self):
        """
        :return all children element
        """
        return self.children_set.all()

    def parents_tree(self):
        if self.parents is not None:
            return [self.parents.id] + self.parents.parents_tree()
        else:
            return [None]


    def save(self, *args, **kwargs):
        tree = self.parents_tree()
        self.hierarchy = ':'.join([str(i) for i in tree if i])
        super(Item, self).save(*args, **kwargs)


    def __str__(self):
        return self.name
