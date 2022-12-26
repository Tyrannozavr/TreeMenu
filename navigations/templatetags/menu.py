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
    nodelist = parser.parse(("endshownodes",))
    parser.delete_first_token()
    return ShowNodesNode(token, nodelist)

class ShowNodesNode(template.Node):
    def __init__(self, token, nodelist):
        self.token = token
        self.nodelist = nodelist

    def render(self, context):
        result = [
            "<ul><li>Token info:</li><ul>",
        ]

        for part in self.token.split_contents():
            content = str(part)
            result.append(f"<li>{content}</li>")

        result.append("</ul><li>Block contents:</li><ul>")
        for node in self.nodelist:
            content = str(node)
            result.append(f"<li>{content}</li>")

        result.append("</ul>")
        return "".join(result)
