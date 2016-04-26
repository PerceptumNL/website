from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                StreamFieldPanel,
                                                InlinePanel,
                                                MultiFieldPanel,
                                                PageChooserPanel)
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

class BlogPageTag(TaggedItemBase):
  content_object = ParentalKey('blog.BlogPage', related_name='tagged_items')

class LinkFields(models.Model):
  link_external = models.URLField("External link", blank=True)
  link_page = models.ForeignKey(
      'wagtailcore.Page',
      null=True,
      blank=True,
      related_name='+'
  )

  @property
  def link(self):
      if self.link_page:
          return self.link_page.url
      else:
          return self.link_external

  panels = [
      FieldPanel('link_external'),
      PageChooserPanel('link_page'),
  ]

  class Meta:
      abstract = True


# Related links
class RelatedLink(LinkFields):
  title = models.CharField(max_length=255, help_text="Link title")

  panels = [
      FieldPanel('title'),
      MultiFieldPanel(LinkFields.panels, "Link"),
  ]

  class Meta:
      abstract = True

class BlogRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('BlogPage', related_name='related_links')

class BlogPage(Page):
  date = models.DateField("Post date")
  main_image = models.ForeignKey(
      'wagtailimages.Image',
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='+'
  )
  tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
  intro = models.CharField(max_length=500, blank=True, default='')
  body = StreamField([
    ('heading', blocks.CharBlock(classname="full title")),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock()),
  ])

  search_fields = Page.search_fields + (
    index.SearchField('intro'),
    index.SearchField('body'),
  )

  content_panels = Page.content_panels + [
    FieldPanel('date'),
    FieldPanel('tags'),
    FieldPanel('intro'),
    StreamFieldPanel('body'),
    InlinePanel('related_links', label="Related links"),
  ]

class BlogIndexPage(Page):
  intro = RichTextField(blank=True)

  content_panels = Page.content_panels + [
      FieldPanel('intro', classname="full")
  ]

  @property
  def blogs(self):
      # Get list of live blog pages that are descendants of this page
      blogs = BlogPage.objects.live().descendant_of(self)

      # Order by most recent date first
      blogs = blogs.order_by('-date')

      return blogs

  def get_context(self, request):
      # Get blogs
      blogs = self.blogs

      # Filter by tag
      tag = request.GET.get('tag')
      if tag:
          blogs = blogs.filter(tags__name=tag)

      # Pagination
      page = request.GET.get('page')
      paginator = Paginator(blogs, 10)  # Show 10 blogs per page
      try:
          blogs = paginator.page(page)
      except PageNotAnInteger:
          blogs = paginator.page(1)
          page = 1
      except EmptyPage:
          blogs = paginator.page(paginator.num_pages)
          page = paginator.num_pages

      # Update template context
      context = super(BlogIndexPage, self).get_context(request)
      context['blogs'] = blogs
      context['pages'] = range(1, paginator.num_pages+1)
      context['pagenumber'] = int(page)
      context['num_pages'] = paginator.num_pages
      return context
