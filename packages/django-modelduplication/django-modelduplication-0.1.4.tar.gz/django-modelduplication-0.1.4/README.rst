=====
Model Duplication
=====

Django admin have `save_as` feature, but that feature have bug with images field, and sometime you want 100% duplication of a model instance with all other related objects and customization, then `save_as` doesn't fit for that purpose.

.. image:: https://coveralls.io/repos/github/squallcs12/django-modelduplication/badge.svg?branch=master
:target: https://coveralls.io/github/squallcs12/django-modelduplication?branch=master


Quick start
-----------

1. Add "modelduplication" to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        # ...  
        'modelduplication',
    ]


2. Define `pre_duplicate` and `post_duplicate` to your models to customize duplication process:

.. code-block:: python

    class Book(models.Model):
        def pre_duplicate(self, origin, first_level):
            """This method use to modify object before `save` on duplication.
            :type origin models.Model
            :type first_level bool
            :param first_level is the root level of duplication
            :param origin the origin instance
            """ 
            pass

        def post_duplicate(self, origin):
            """This method is called after finishing the duplication.
            :type origin models.Model
            :param origin the origin instance
            """ 
            pass
