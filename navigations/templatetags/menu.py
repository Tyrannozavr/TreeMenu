from django import template

register = template.Library()

@register.inclusion_tag('tags/menu.html')
def draw_menu(value):
    # print(value, type(value))
    return {'value': value}

@register.inclusion_tag('tags/results.html')
def show_results(poll):
    return {'choices': poll}

@register.tag()
def shownodes(parser, token):
    # print('parser', parser, ': ', token)
    # print('show')
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
        lst = [[i for i in range(4)] for i in range(3)]
        menu = create_tree(lst)
        print('menu', menu)
        return menu
        # content = []
        # print('render')
        # for part in self.token.split_contents():
        #     part = str(part)
            # print('part', part)
            # content.append('<li>'+part+'</li>')
        # menu = create_tree(3)
        # content.append(menu)
        # print(content)
        # return "<ul>"+"".join(content)+"</ul>"
