from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                InlinePanel,
                                                MultiFieldPanel,
                                                PageChooserPanel,
                                                StreamFieldPanel)
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey

class HomePage(Page):
  about_title = models.CharField(max_length=255)
  about = RichTextField()
  contact_form = models.ForeignKey(
      'forms.FormPage',
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='+',
  )


  content_panels = [
    InlinePanel('taglines', label="Tag lines"),
    FieldPanel('about_title'),
    FieldPanel('about'),
    InlinePanel('features', label="Features"),
    PageChooserPanel('contact_form'),
  ]


class HomePageFeature(Orderable):
  page = ParentalKey(HomePage, related_name='features')
  title = models.CharField(max_length=255)
  body = RichTextField()
  read_more_page = models.ForeignKey(
      'wagtailcore.Page',
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='+',
  )

  panels = [
    FieldPanel('title'),
    FieldPanel('body'),
    PageChooserPanel('read_more_page')
  ]


class HomePageTagLines(Orderable):
  page = ParentalKey(HomePage, related_name='taglines')
  title = models.CharField(max_length=255)
  body = RichTextField()
  cover = models.ForeignKey(
      'wagtailimages.Image',
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='+'
  )
  read_more_page = models.ForeignKey(
      'wagtailcore.Page',
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='+',
  )

  panels = [
    FieldPanel('title'),
    FieldPanel('body'),
    ImageChooserPanel('cover'),
    PageChooserPanel('read_more_page')
  ]

class StandardPage(Page):
  body = StreamField([
    ('heading', blocks.CharBlock(classname="full title")),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock()),
  ])

  search_fields = Page.search_fields + (
    index.SearchField('body'),
  )

  content_panels = Page.content_panels + [
    StreamFieldPanel('body'),
  ]
