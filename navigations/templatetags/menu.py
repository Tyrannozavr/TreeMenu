from django import template

register = template.Library()

@register.inclusion_tag('tags/menu.html')
def draw_menu(value):
    print(value, type(value))
    return {'value': value}

@register.inclusion_tag('tags/results.html')
def show_results(poll):
    return {'choices': poll}

@register.tag()
def shownodes(parser, token):
    print('parser', parser, ': ', token)
    parser.delete_first_token()
    return ShowNodesNode(token)

class ShowNodesNode(template.Node):
    def __init__(self, token):
        self.token = token

    def render(self, context):
        content = []
        for part in self.token.split_contents():
            part = str(part)
            content.append('<li>'+part+'</li>')
        return "<ul>"+"".join(content)+"</ul>"
