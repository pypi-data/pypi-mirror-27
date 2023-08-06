from django.conf import settings
from django.template.loader import render_to_string, TemplateDoesNotExist

APP_BASE_DIR = settings.BASE_DIR + '/hx_toolkit/'
STATIC_OUTPUT_DIR = APP_BASE_DIR + 'static/hx_toolkit_output/'
ARTICLE_OUTPUT_DIR = APP_BASE_DIR + 'templates/hx_toolkit_output/'
ARTICLE_BY_SLUG_DIR = ARTICLE_OUTPUT_DIR + "by_id/"
ARTICLE_BY_WEEK_DIR = ARTICLE_OUTPUT_DIR + "weekly/"
SUMMARY_LINKS_DIR = ARTICLE_OUTPUT_DIR + "summary/"


def get_article_links_by_category():
    category_data = {'know-yourself': _get_category_by_id('know-yourself'),
                     'make-your-way': _get_category_by_id('make-your-way'),
                     'weave-together': _get_category_by_id('weave-together'),
                     'know-world': _get_category_by_id('know-world')
                     }
    return category_data


def _get_category_by_id(id):
    path = 'hx_toolkit_output/summary/' + id + ".html"
    try:
        return render_to_string(path)
    except TemplateDoesNotExist:
        return None


def get_article_by_id(article_id):
    article_path = ARTICLE_OUTPUT_DIR + article_id + ".html"

    try:
        with open(article_path, 'r') as article_file:
            article_data = article_file.read()
            return article_data
    except IOError:
        return None


def get_rendered_article_by_id(article_id):
    article_file = "hx_toolkit_output/by_id/" + article_id + ".html"
    return render_to_string(article_file)


def get_article_by_phase_quarter_week(phase, quarter, week):
    week = str(week)
    root = "hx_toolkit_output/weekly/"

    path = root + phase + "/" + quarter + "/" + week + ".html"

    try:
        return render_to_string(path)
    except TemplateDoesNotExist:
        return None
