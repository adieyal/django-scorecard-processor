from django.template import defaulttags, Library, Node, Token

register = Library()

@register.tag
def nav_url(parser, token):
    name, url, title = token.split_contents()
    url = defaulttags.url(parser, Token(token.token_type, 'url %s' % url))
    return NavNode(url, title)
    
class NavNode(Node):
    def __init__(self, url_node, title):
        self.url_node, self.title = url_node, title
        
    def render(self, context):
        url = self.url_node.render(context)
        classes = ""
        if context['request'].path == url:
            classes = 'active'
        return """
            <li class="%s">
                <a href="%s">
                    %s
                </a>
            </li>
        """ % (classes, url, self.title[1:-1])

