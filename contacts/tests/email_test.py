# coding=utf-8
from __future__ import unicode_literals
import pytest

from django.core import mail

from contacts.forms import UpdateContactForm

from .factories import UserFactory


def generate_form_with_data(formclass, instance):
    form = formclass(instance=instance)
    available_fields = form.changed_data
    form_data = {}
    for field in available_fields:
        form_data[field] = getattr(instance, field)
    # Now instantiate form with data
    formwithdata = formclass(instance=instance, data=form_data)
    return formwithdata


@pytest.mark.integration
@pytest.mark.django_db
def test_saving_a_contact_does_not_send_email_change_if_no_password():
    assert len(mail.outbox) == 0
    u = UserFactory()
    u.set_unusable_password()
    form = generate_form_with_data(UpdateContactForm, u)
    form.data['business_email'] = 'newemail@test.com'
    form.is_valid()
    form.save()
    assert len(mail.outbox) == 0


@pytest.mark.integration
@pytest.mark.django_db
def test_saving_a_contact_sends_email_change_if_password_check_contents():
    assert len(mail.outbox) == 0
    u = UserFactory()
    u.set_password('åρｒｏｐｅｒρäѕｓɰòｒｄ')
    form = generate_form_with_data(UpdateContactForm, u)

    old_email = u.business_email
    new_email = 'newemail@test.com'
    # change the email
    form.data['business_email'] = new_email
    # save the form
    form.is_valid()
    form.save()
    # Test
    email = mail.outbox[0]
    assert email.to == [old_email, new_email]
    assert new_email in email.body
    assert old_email in email.body
