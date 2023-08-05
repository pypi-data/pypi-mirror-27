situation
=============

**situation** is a Python package that provides the Situation Modeling Language (SML) - an ontology for describing social situations.

.. image:: https://img.shields.io/github/stars/iandennismiller/situation.svg?style=social&label=GitHub
    :target: https://github.com/iandennismiller/situation

.. image:: https://img.shields.io/pypi/v/situation.svg
    :target: https://pypi.python.org/pypi/situation

.. image:: https://readthedocs.org/projects/situation/badge/?version=latest
    :target: http://situation.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/iandennismiller/situation.svg?branch=master
    :target: https://travis-ci.org/iandennismiller/situation

.. image:: https://coveralls.io/repos/github/iandennismiller/situation/badge.svg?branch=master
    :target: https://coveralls.io/github/iandennismiller/situation?branch=master

Overview
--------

The following is a full Situation in which Alice and Bob are members of a Sports Club.
When this code is executed, a situation will be created within the database and will then be printed to the screen.

::

    from situation import dump, Person, Group
    from situation.debug_app import quick
    with quick().app_context():
        bob = Person.create(name="Bob")
        alice = Person.create(name="Alice")
        club = Group.create(name="Sports Club")
        club.members.extend([bob, alice])
        print(dump())

A situation is specified using Situation Modeling Language (SML).
SML is like a Domain Specific Language for Situations built on top of Python.

A Situation is actually a full database-driven `Flask-Diamond <http://flask-diamond.org>`_ application.
As an application, this can be an extremely flexible data platform.

Installation
^^^^^^^^^^^^

Install **situation** using Python pip.

::

    pip install situation

Documentation
^^^^^^^^^^^^^

http://situation.readthedocs.io

