from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.models import Orderable
from modelcluster.fields import ParentalKey

class HomePage(Page):
  about_title = models.CharField(max_length=255)
  about = RichTextField()


  content_panels = [
    InlinePanel('taglines', label="Tag lines"),
    FieldPanel('about_title'),
    FieldPanel('about'),
    InlinePanel('features', label="Features")
  ]


class HomePageFeature(Orderable):
  page = ParentalKey(HomePage, related_name='features')
  title = models.CharField(max_length=255)
  body = RichTextField()

  panels = [
    FieldPanel('title'),
    FieldPanel('body')
  ]


class HomePageTagLines(Orderable):
  page = ParentalKey(HomePage, related_name='taglines')
  title = models.CharField(max_length=255)
  body = RichTextField()

  panels = [
    FieldPanel('title'),
    FieldPanel('body')
  ]
