=====
Note
=====

Note is a simple Django app to conduct Web-based notes.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "note" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'note',
    ]

2. Include the todo URLconf in your project urls.py like this::

    url(r'^note/', include(note.urls, namespace='note')),

3. Run `python manage.py migrate` to create the note models.

4. Start the project's server and login on your django-website.

5. Visit https://your_django_website_url_part/note/ to use the note app.
