======
Notice
======

This is a fork of django-bootstrap3, which includes modifications for INFINIDAT's look and feel.
There are small changes in form rendering, as well as three CSS files which should be
included after Bootstrap itself:

- infiniboot.css
- infinidat.css
- opensans.css

Themed components include:

- Buttons
- Labels
- Forms
- Custom checkboxes and radio buttons
- Wells
- Navbars (inverse only)
- Tables
- Tabs
- Pills
- Modals


Themed Checkboxes
-----------------

Here's the markup required for a themed checkbox::

    <div class="themed-checkbox">
        <label>
            <input type="checkbox" name="agree">
            <span></span>
            I agree to the terms and conditions
        </label>
    </div>


Releasing a new version
-----------------------

- Edit the version number in bootstrap3/__init__.py
- Run ``python setup.py sdist upload -r local``


======================
Bootstrap 3 for Django
======================

Write Django as usual, and let ``django-bootstrap3`` make template output into Bootstrap 3 code.


Requirements
------------

- Python 2.7, 3.2, 3.3, 3.4, or 3.5
- Django >= 1.8

*The latest version supporting Python 2.6 and Django < 1.8 is the 6.x.x branch.*


Installation
------------

1. Install using pip:

   ``pip install django-bootstrap3``

   Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to INSTALLED_APPS in your ``settings.py``:

   ``'bootstrap3',``

3. In your templates, load the ``bootstrap3`` library and use the ``bootstrap_*`` tags:

This app will soon require Django 1.8+, python 2.7+. Thanks for understanding.


Example template
----------------

   .. code:: Django

    {% load bootstrap3 %}

    {# Display a form #}

    <form action="/url/to/submit/" method="post" class="form">
        {% csrf_token %}
        {% bootstrap_form form %}
        {% buttons %}
            <button type="submit" class="btn btn-primary">
                {% bootstrap_icon "star" %} Submit
            </button>
        {% endbuttons %}
    </form>


Documentation
-------------

The full documentation is at http://django-bootstrap3.readthedocs.org/.


Bugs and suggestions
--------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/dyve/django-bootstrap3/issues


License
-------

You can use this under Apache 2.0. See `LICENSE
<LICENSE>`_ file for details.


Author
------

Developed and maintained by `Zostera <https://zostera.nl/>`_.

Original author & Development lead: `Dylan Verheul <https://github.com/dyve>`_.

Thanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.

Please see AUTHORS.rst for a list of contributors.