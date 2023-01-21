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
    hierarchy = models.ManyToManyField('self', null=True, blank=True, auto_created=True)

    def children(self):
        """
        :return all children element
        """
        return self.children_set.all()

    def family_tree(self):
        """
        :return: returns a list of parent ids up to the root element
        """
        if self.parents is None:
            return []
        else:
            return self.parents.family_tree() + [self.parents.id]

    def parents_tree(self):
        if not self.parents:
            return [self]
        else:
            return [self] + self.parents.parents_tree()


    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        print('before', Item.objects.get(name='5').hierarchy.all())
        tree = self.parents_tree()
        print('middle', Item.objects.get(name='5').hierarchy.all())
        # self.hierarchy.add(*tree)
        self.hierarchy.add(tree[0])
        print('check', self.name)
        print('after', Item.objects.get(name='5').hierarchy.all())


    def __str__(self):
        return self.name
