from django.contrib.auth import get_user_model


USER_MODEL = get_user_model()


class Permissions(object):
    #================================================================
    # Custom Permissions
    #================================================================
    '''
    Defined here and not in class Meta because South doesn't handle
    that yet and we would need to run syncdb --all on deployment.

    Check if this is still true on Django 1.7
    '''
    custom_permissions = [
        # (codename,     name,      model(for content_type))
        ('add_personal_info', 'Add personal info', USER_MODEL),
    ]

    #================================================================
    # Group permissions
    #================================================================
    group_permissions = {
        'Contacts managers': (
            (USER_MODEL, 'add_personal_info'),
            (USER_MODEL, 'add_user'),
            (USER_MODEL, 'change_user'),
            (USER_MODEL, 'delete_user')
        )
    }
