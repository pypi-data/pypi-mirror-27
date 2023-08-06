from django.core.management.base import BaseCommand, CommandError
from hx_toolkit.db_dao import get_article_by_slug, create_article_data
from hx_toolkit.views import render_article_html
from hx_toolkit.models import Article
from django.conf import settings
import json
import os
import shutil


class Command(BaseCommand):

    def handle(self, *args, **options):
        data_dir = settings.THRIVE_OUTPUT
        article_dir = data_dir + "/articles/"

        # Ensure article dir exists and is empty
        if os.path.exists(article_dir):
            shutil.rmtree(article_dir)
        os.mkdir(article_dir)

        summary_data = create_article_data()
        summary_json_data = json.dumps(summary_data)
        summary_path = data_dir + "/summary.json"

        with open(summary_path, 'w') as summary_file:
                summary_file.write(summary_json_data.encode('utf-8'))

        load_static_string = "{% load static %}"
        articles = Article.objects.all()
        for article in articles:
            rel_path = self._move_image(article.image.path)
            image_static_string = self._get_static_string(rel_path)
            setattr(article, 'image_static_string', image_static_string)
            setattr(article, 'load_static_string', load_static_string)

            article_long_html = render_article_html(article)

            base = settings.BASE_DIR
            article_dir = base + "/hx_toolkit/templates/hx_toolkit_output/"
            article_path = article_dir + article.get_article_filename()
            with open(article_path, 'w+') as article_file:
                article_file.write(article_long_html.encode('utf-8'))

            if article.short_body:
                article_short_html = render_article_html(article, True)
                article_path = article_dir + article.get_article_filename(True)
                with open(article_path, 'w+') as article_file:
                    article_file.write(article_short_html.encode('utf-8'))

    def _move_image(self, image_path):
        filename = os.path.basename(image_path)
        base = settings.BASE_DIR
        images_dir = 'hx_toolkit_images'

        new_path = '{}/hx_toolkit/static/{}/{}'.format(base,
                                                       images_dir,
                                                       filename)
        shutil.copyfile(image_path, new_path)

        rel_path = '{}/{}'.format(images_dir, filename)

        return rel_path

    def _get_static_string(self, image_path):
        string = "{% static '" + image_path + "' %}"
        return string
