from django import template
register = template.Library()

@register.filter
def is_field_type(field, typestr):
  from django.forms import widgets
  type_widgets = {
    'text': widgets.TextInput,
    'number': widgets.NumberInput,
    'email': widgets.EmailInput,
    'url': widgets.URLInput,
    'password': widgets.PasswordInput,
    'hidden': widgets.HiddenInput,
    'date': widgets.DateInput,
    'datetime': widgets.DateTimeInput,
    'time': widgets.TimeInput,
    'textarea': widgets.Textarea,
    'checkbox': widgets.CheckboxInput,
    'select': widgets.Select,
    'select-multiple': (widgets.SelectMultiple,
                        widgets.CheckboxSelectMultiple),
    'radio': widgets.RadioSelect,
    'file': (widgets.FileInput, widgets.ClearableFileInput),
  }
  if isinstance(type_widgets[typestr], tuple):
    return any([isinstance(field.field.widget, widget) \
        for widget in type_widgets[typestr]])
  else:
    return isinstance(field.field.widget, type_widgets.get(typestr))

@register.inclusion_tag('forms/form_page.html', takes_context=True)
def display_ajax_form(context, form_page, submit_btn_class=None):
  return {'form': form_page.get_form(),
          'form_class': 'ajax-form',
          'submit_url': form_page.url,
          'submit_text': form_page.submit_text,
          'submit_btn_class': submit_btn_class or '',
          'csrf_token': context['csrf_token']}
