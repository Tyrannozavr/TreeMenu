from django import template

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


def create_tree(lst):
    answer = []
    answer.append('<ul>')
    for i in lst:
        if type(i) is list:
            answer.append(create_tree(i))
        else:
            answer.append('<li>'+str(i)+'</li>')
    answer.append('</ul>')
    return ''.join(answer)

class ShowNodesNode(template.Node):
    def __init__(self, token):
        self.token = token

    def render(self, context):
        lst = [1, 2, [12, 13, 14], [15, 16, [22, 33]], 3]
        menu = create_tree(lst)
        return menu
