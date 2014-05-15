invite-registration-contacts
============================

A companion app to invite-registration for basic management of users outside of Django's admin interface. invite-registration is a Django app for managing users and their registration when you need to control creation of accounts, but it is up to users to activate them by creating passwords.

invite-registration-contacts adds a role of contact manager so adding, updating, removing and inviting users can be done outside of the admin interface.

WARNING
-------
This app has not been widely tested yet so proceed with caution.


Installation
------------
Install requirements listed in ``requirements.txt``. Also add this app's code somewhere where Django can find it. Then add ``contacts`` to the ``INSTALLED_APPS`` list in your settings file and include ``contacts.urls`` where you want the app to reside.
