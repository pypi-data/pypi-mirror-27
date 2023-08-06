from django.core.management.base import BaseCommand, CommandError
from hx_toolkit.db_dao import get_article_by_slug, create_article_data
from hx_toolkit.file_dao import STATIC_OUTPUT_DIR, ARTICLE_OUTPUT_DIR, \
    ARTICLE_BY_SLUG_DIR, ARTICLE_BY_WEEK_DIR, SUMMARY_LINKS_DIR
from hx_toolkit.views import render_article_html, render_category_links
from hx_toolkit.models import Article
import json
import os
import shutil
from PIL import Image


class Command(BaseCommand):
    IMAGE_OUTPUT_DIR = STATIC_OUTPUT_DIR + 'images/'
    IMAGE_REL_DIR = 'hx_toolkit_output/images/'
    IMAGE_WIDTHS = [480, 650, 780, 1000]

    def _render_articles(self, articles):
        load_static_string = "{% load static %}"
        articles_by_category = {}

        for article in articles:
            srcset_paths = {}
            for width in self.IMAGE_WIDTHS:
                path = self._move_image(article.image.path, width)
                image_static_string = self._get_static_string(path)
                srcset_paths[width] = image_static_string

            setattr(article, 'image_srcset_paths', srcset_paths)
            setattr(article, 'load_static_string', load_static_string)

            cs = article.category.slug
            articles_by_category.setdefault(cs, [])

            articles_by_category[cs].append({'slug': article.slug,
                                             'title': article.title})

            article_long_html = render_article_html(article)
            article_short_html = render_article_html(article, True)

            # save article by slug
            article_path = ARTICLE_BY_SLUG_DIR + article.get_article_filename()
            self._save_html(article_long_html, article_path)

            # save article by week path
            if article.phase:
                week_path = ARTICLE_BY_WEEK_DIR + \
                            article.phase + "/" + \
                            article.quarter + "/"
                if not os.path.exists(week_path):
                    os.makedirs(week_path)
                week_path += str(article.week) + ".html"
                self._save_html(article_short_html, week_path)

        for category in articles_by_category:
            links = articles_by_category[category]
            rendered_links = render_category_links(links)
            self._save_html(rendered_links, SUMMARY_LINKS_DIR +
                            category + ".html")

    def _save_html(self, html, path):
        with open(path, 'w+') as article_file:
            article_file.write(html.encode('utf-8'))

    def handle(self, *args, **options):
        # Ensure directories exist and are empty
        self._create_or_empty_dir(STATIC_OUTPUT_DIR)
        self._create_or_empty_dir(self.IMAGE_OUTPUT_DIR)
        self._create_or_empty_dir(ARTICLE_OUTPUT_DIR)
        self._create_or_empty_dir(ARTICLE_BY_SLUG_DIR)
        self._create_or_empty_dir(ARTICLE_BY_WEEK_DIR)
        self._create_or_empty_dir(SUMMARY_LINKS_DIR)

        """
        Article File Structure
        templates/hx_toolkit_output
            /by_slug
                [slug].html -Flat list of all -long articles
            /categories/
                [category_slug].html -Category card HTML, list of article links
            /weekly/
                /[phase]
                    /[quarter]
                        [week].html -Short version of weekly articles
        """
        articles = Article.objects.all()
        self._render_articles(articles)

    def _move_image(self, image_path, width):
        filename = os.path.basename(image_path)

        resized_image = self._resize_image(image_path, width)

        file, ext = os.path.splitext(filename)
        resized_filename = file + "_" + str(width) + ext

        new_path = self.IMAGE_OUTPUT_DIR + resized_filename
        resized_image.save(new_path)

        rel_path = self.IMAGE_REL_DIR + resized_filename

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

    def _resize_image(self, image_path, width):
        image = Image.open(image_path)
        width_percent = (width / float(image.size[0]))
        height = int((float(image.size[1]) * float(width_percent)))
        image = image.resize((width, height), Image.ANTIALIAS)

        return image
