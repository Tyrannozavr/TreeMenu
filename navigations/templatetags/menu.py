from django import template
from navigations import models


register = template.Library()

@register.inclusion_tag('tags/menu.html')
def draw_menu(value):
    return {'value': value}

@register.inclusion_tag('tags/results.html')
def show_results(poll):
    return {'choices': poll}

@register.tag()
def shownodes(parser, token):
    parser.delete_first_token()
    return ShowNodesNode(token)

def create_tree(array, item, children=None):
    print(item, '...', children)
    if not item.parents:
        parallel = list(array.filter(parents__isnull=True))
        parallel.insert(parallel.index(item) + 1, children)
        return parallel

    if not children:
        children = list(item.children_set.all())
    parallel = list(item.parents.children_set.all())
    parallel.insert(parallel.index(item) + 1, children)
    print(children)
    array = create_tree(array, item.parents, parallel)
    return array

def create_menu(lst):
    answer = []
    answer.append('<ul>')
    for i in lst:
        if type(i) is list:
            answer.append(create_menu(i))
        else:
            answer.append('<li>'+str(i)+'</li>')
    answer.append('</ul>')
    return ''.join(answer)

class ShowNodesNode(template.Node):
    def __init__(self, token):
        self.token = token

    def render(self, context):
        array = models.Item.objects.filter(menu=models.Menu.objects.first())
        item = array.get(name='1.1.11')
        lst = create_tree(array, item)
        print(lst)
        menu = create_menu(lst)
        return menu
