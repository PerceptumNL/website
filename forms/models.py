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
      self.request = request
      return super().serve(request)

    def process_form_submission(self, form):
        super(AbstractEmailForm, self).process_form_submission(form)

        if self.to_address:
          from django.template import Context
          from django.template.loader import get_template
          from django.core.mail import send_mail

          context = Context({
            'items': [(x[1].label, form.data.get(x[0])) \
                for x in form.fields.items()],
            'title': self.title,
            'referer': self.request.META.get('HTTP_REFERER', '-')
          })
          html_content = get_template(
            'forms/form_onsubmit_email.html').render(context)
          plain_content = get_template(
            'forms/form_onsubmit_email_plain.txt').render(context)

          send_mail(self.subject, plain_content, self.from_address,
                    [self.to_address], html_message=html_content)
