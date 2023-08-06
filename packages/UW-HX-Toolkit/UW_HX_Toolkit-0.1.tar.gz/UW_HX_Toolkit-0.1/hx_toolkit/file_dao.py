from django.conf import settings
import json
from django.template.loader import render_to_string


def _get_article_data():
    data_dir = settings.THRIVE_OUTPUT
    summary_path = data_dir + "/summary.json"

    with open(summary_path, 'r') as summary_file:
        json_data = summary_file.read()
        thrive_data = json.loads(json_data)
        return thrive_data


def get_article_links_by_category():
    thrive_data = _get_article_data()
    return thrive_data['category']


def get_article_by_id(article_id):
    data_dir = settings.THRIVE_OUTPUT

    article_path = data_dir + "/articles/" + article_id + ".html"

    try:
        with open(article_path, 'r') as article_file:
            article_data = article_file.read()
            return article_data
    except IOError:
        return None


def get_rendered_article_by_id(article_id, is_short=False):
    if is_short:
        article_file = "hx_toolkit_output/" + article_id + "_short.html"
    else:
        article_file = "hx_toolkit_output/" + article_id + "_long.html"
    return render_to_string(article_file)


def get_article_by_phase_quarter_week(phase, quarter, week):
    article_data = _get_article_data()
    try:
        article = article_data['time'][phase][quarter][str(week)]['slug']

        return get_rendered_article_by_id(article, True)
    except KeyError:
        return None
