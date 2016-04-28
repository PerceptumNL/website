from django import template
from blog.models import *

register = template.Library()

@register.inclusion_tag('blog/blog_list.html')
def list_blogs(blogs=None, max_num=10):
  if blogs is None:
    blogs = BlogPage.objects.live().order_by('-date')[:max_num]
  return {'blogs': blogs}

def list_blogs_under_page(page, max_num=10):
  return list_blogs(BlogPage.objects.live().descendant_of(page), max_num)

def list_blogs_with_tag(tag, max_num=10):
  return list_blogs(BlogPage.objects.live().filter(tags__name=tag), max_num)
