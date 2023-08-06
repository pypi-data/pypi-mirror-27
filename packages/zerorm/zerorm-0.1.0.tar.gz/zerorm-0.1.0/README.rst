Zerorm
======

Zerorm is a simple wrapper for three amazing packages. This repository is the
place where `TinyDB <https://github.com/msiemens/tinydb>`_, `Schematics <https://github.com/schematics/schematics>`_
and `Lifter <https://github.com/EliotBerriot/lifter>`_ together look like Django ORM.

It's still work in progress and not everything looks like Django ORM, but it will.

Installation
------------

.. code-block:: shell

     pip install zerorm

Usage
-----

First create a *models.py* file with database instance (TinyDB) attached to model (Schematics):

.. code-block:: python

    from zerorm import db, models

    database = db('db.json')


    class Message(models.Model):
        author = models.StringType(required=True)
        author_email = models.EmailType()
        text = models.StringType()
        stars = models.IntType(min_value=0, max_value=5)

        class Meta:
            database = database

Now create some objects:

.. code-block:: pycon

    >>> from models import Message
    >>>
    >>> bob_message = Message(author='Bob',
    ...                       author_email='bob@example.com',
    ...                       text='Hello, everyone!')
    >>> bob_message
    <Message: Message object>
    >>> bob_message.save()  # Save object
    1
    >>>
    >>> bob_message.stars = 3
    >>> bob_message.save()  # Update object
    >>>
    >>> alice_message = Message.objects.create(author='Alice',
    ...                                        text='Hi, Bob!',
    ...                                        stars=0)
    >>> alice_message
    <Message: Message object>

And try to retrieve them via *.objects* (DataManger with Lifter)

.. code-block:: pycon

    >>> Message.objects.all()
    [<Message: Message object>, <Message: Message object>]
    >>> first_message = Message.objects.get(eid=1)
    >>> first_message.author
    'Bob'
    >>> Message.objects.filter(stars__gte=3)  # Only Bob's message has 3 stars
    [<Message: Message object>]

You can also redefine model's __str__ method for better repr just like in Django.

.. code-block:: python

    class Message(models.Model):
        ...

        def __str__(self):
            return 'by {}'.format(self.author)

.. code-block:: pycon

    >>> Message.objects.all()
    [<Message: by Bob>, <Message: by Alice>]

License
-------

MIT. See LICENSE for details.