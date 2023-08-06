from django.core.management.base import BaseCommand, CommandError
from hx_toolkit.db_dao import get_article_by_slug, create_article_data
from hx_toolkit.file_dao import STATIC_OUTPUT_DIR, ARTICLE_OUTPUT_DIR
from hx_toolkit.views import render_article_html
from hx_toolkit.models import Article
from django.conf import settings
import json
import os
import shutil


class Command(BaseCommand):
    IMAGE_OUTPUT_DIR = STATIC_OUTPUT_DIR + 'images/'
    IMAGE_REL_DIR = 'hx_toolkit_output/images/'

    def handle(self, *args, **options):
        # Ensure directories exist and are empty
        self._create_or_empty_dir(STATIC_OUTPUT_DIR)
        self._create_or_empty_dir(self.IMAGE_OUTPUT_DIR)
        self._create_or_empty_dir(ARTICLE_OUTPUT_DIR)
        summary_data = create_article_data()
        summary_json_data = json.dumps(summary_data)
        summary_path = STATIC_OUTPUT_DIR + "/summary.json"

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

            article_path = ARTICLE_OUTPUT_DIR + article.get_article_filename()
            with open(article_path, 'w+') as article_file:
                article_file.write(article_long_html.encode('utf-8'))

            if article.short_body:
                article_short_html = render_article_html(article, True)
                article_filename = article.get_article_filename(True)
                article_path = ARTICLE_OUTPUT_DIR + article_filename
                with open(article_path, 'w+') as article_file:
                    article_file.write(article_short_html.encode('utf-8'))

    def _move_image(self, image_path):
        filename = os.path.basename(image_path)

        new_path = self.IMAGE_OUTPUT_DIR + filename
        shutil.copyfile(image_path, new_path)

        rel_path = self.IMAGE_REL_DIR + filename

        return rel_path

    def _get_static_string(self, image_path):
        string = "{% static '" + image_path + "' %}"
        return string

    def _create_or_empty_dir(self, dir_path):
        try:
            shutil.rmtree(dir_path)
        except OSError:
            pass
        os.makedirs(dir_path)
