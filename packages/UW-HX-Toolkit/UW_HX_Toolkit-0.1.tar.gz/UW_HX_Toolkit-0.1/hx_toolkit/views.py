from django.template.loader import render_to_string


def render_article_html(article, is_short=False):
    template = 'message_long.html'
    if is_short:
        template = 'message_short.html'
    article_string = render_to_string(template, {'article': article})
    return article_string
