from django.conf import settings
from django.forms import (
    ModelForm, HiddenInput, ImageField
)
import floppyforms as forms
from form_utils.forms import BetterModelForm
from registration import mail
from registration.models import User
from .widgets import (
    BetterFileInput,
    BetterImageInput,
)

TITLES = (
    'Dr', 'Hon', 'Mrs', 'Ms', 'Mr', 'Prof', 'His Excellency',
    'Her Excellency', 'Rt.Hon', 'Assoc. Prof'
)


class TitleInput(forms.TextInput):
    def get_context_data(self):
        ctx = super(TitleInput, self).get_context_data()
        ctx.update({
            'datalist': TITLES
        })
        return ctx


#######################################################################
# Contacts forms
#######################################################################
class UpdatePersonalInfoForm(BetterModelForm):
    picture = ImageField(required=False, widget=BetterImageInput())

    class Meta:
        model = User
        fieldsets = [('all', {'fields': [
            'business_email', 'title', 'first_name',
            'last_name', 'personal_email',
            # Address
            'home_address', 'business_address', 'country', 'nationality',
            # Personal info
            'gender', 'contact_type',
            # Work
            'job_title', 'area_of_specialisation',
            # Phones & fax
            'home_tel', 'business_tel', 'mobile', 'fax',
            # IM
            'skype_id', 'yahoo_messenger', 'msn_id',
            'notes', 'picture', 'cv']})]

        widgets = {
            'title': TitleInput,
            'cv': BetterFileInput
        }


class AddContactForm(BetterModelForm):
    picture = ImageField(required=False, widget=BetterImageInput())

    class Meta:
        model = User
        fieldsets = [
            ('all', {'fields':
                    ['business_email', 'title', 'first_name',
                     'last_name', 'personal_email', 'is_active',
                     # Address
                     'home_address', 'business_address', 'country',
                     'nationality',
                     # Personal info
                     'gender',
                     # Work
                     'job_title', 'area_of_specialisation',
                     # Phones & fax
                     'home_tel', 'business_tel', 'mobile', 'fax',
                     # IM
                     'skype_id', 'yahoo_messenger', 'msn_id',
                     'notes', 'picture', 'cv']})
        ]
        widgets = {
            'title': TitleInput,
            'cv': BetterFileInput
        }


class UpdateContactForm(AddContactForm):
    def notify_email_change(self,
                            old_address,
                            new_address,
                            subject='{0}: email change notification'.format(
                                settings.SITE_NAME),
                            template_name='registration/email/email_changed_body.email'):
        ctx = {
            'user': self.instance,
            'old_email': old_address,
            'new_email': new_address
        }
        options = {
            'subject': subject,
            'to': [old_address, new_address],
            'template_name': template_name,
            'context': ctx
        }
        mail.notify(options)

    def save(self, *args, **kwargs):
        if self.instance and self.instance.has_usable_password():
            old = self._meta.model.objects.get(pk=self.instance.pk)
            old_email = old.business_email
            if self.cleaned_data['business_email'] != old_email:
                self.notify_email_change(
                    old_email,
                    self.cleaned_data['business_email'])
        return super(UpdateContactForm, self).save(*args, **kwargs)


class DeleteContactForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(DeleteContactForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget = HiddenInput()

    class Meta:
        model = User
        fields = ('id',)
