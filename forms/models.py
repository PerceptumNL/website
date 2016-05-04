from django.db import models
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                InlinePanel,
                                                MultiFieldPanel)
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')

class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    submit_text = models.CharField(max_length=100, default='Versturen')
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        FieldPanel('submit_text', classname="full"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email")
    ]

    def serve(self, request):
      from django.shortcuts import render
      if request.method == 'POST':
        form = self.get_form(request.POST)

        if form.is_valid():
          self.process_form_submission(form)

          # render the landing_page
          # TODO: It is much better to redirect to it
          resp = render(
              request,
              self.landing_page_template,
              self.get_context(request)
          )
          resp['X-Form-Status'] = 'valid'
          return resp
      else:
        form = self.get_form()

      context = self.get_context(request)
      context['form'] = form
      return render(
        request,
        self.template,
        context
      )

