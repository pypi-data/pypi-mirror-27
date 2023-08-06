from django.conf import settings
import json
from django.template.loader import render_to_string

APP_BASE_DIR = settings.BASE_DIR + '/hx_toolkit/'
STATIC_OUTPUT_DIR = APP_BASE_DIR + 'static/hx_toolkit_output/'
ARTICLE_OUTPUT_DIR = APP_BASE_DIR + 'templates/hx_toolkit_output/'


def _get_article_data():
    summary_path = STATIC_OUTPUT_DIR + "/summary.json"

    with open(summary_path, 'r') as summary_file:
        json_data = summary_file.read()
        thrive_data = json.loads(json_data)
        return thrive_data


def get_article_links_by_category():
    thrive_data = _get_article_data()
    return thrive_data['category']


def get_article_by_id(article_id):
    data_dir = settings.THRIVE_OUTPUT

    article_path = ARTICLE_OUTPUT_DIR + article_id + ".html"

    try:
        with open(article_path, 'r') as article_file:
            article_data = article_file.read()
            return article_data
    except IOError:
        return None


def get_rendered_article_by_id(article_id, is_short=False):
    if is_short:
        article_file = ARTICLE_OUTPUT_DIR + article_id + "_short.html"
    else:
        article_file = ARTICLE_OUTPUT_DIR + article_id + "_long.html"
    return render_to_string(article_file)


def get_article_by_phase_quarter_week(phase, quarter, week):
    article_data = _get_article_data()
    try:
        article = article_data['time'][phase][quarter][str(week)]['slug']

        return get_rendered_article_by_id(article, True)
    except KeyError:
        return None
