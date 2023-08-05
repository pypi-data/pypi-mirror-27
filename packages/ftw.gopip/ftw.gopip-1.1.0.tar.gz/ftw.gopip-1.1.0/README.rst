ftw.gopip
=========

Plone's ``getObjPositionInParent`` catalog index is optimized for fast writing
and for sorting *small* result sets of objects which are loaded anyway in the request.
The actual order is not stored in the catalog at all but only on the parent object.
This means that sorting a result set can only be done by loading the parent object
and getting the object position from it.

This works well for Plone's standard use cases such as the navigation portlet
or the portal tabs, but doing large queries with a bigger depth is very slow
since all container objects must be woken up.

The goal of this package is to replace the ``getObjPositionInParent`` with an actual
index storing the order in the catalog in a regular ``FieldIndex``.


Compatibility
-------------

Plone 4.3.x
Plone 5.1.x


Installation
------------

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.gopip

- Install the generic setup profile ``ftw.gopip:default``.


Implementation
--------------

This package replaces the ``GopipIndex``, which is a fake index not storing any
data, with a ``FieldIndex``, which stores all positions.

The challenge is to keep the index properly up to date.
This is achieved by customizing the standard ``IOrdering`` adapters and tracking
changes there, so that we do not need to rely on other components triggering
events at the right moment.

The three standard ``IOrdering`` adapters are wrapped with a tracking proxy:

- ``DefaultOrdering`` (providing ``IExplicitOrdering``)
- ``PartialOrdering`` (providing ``IExplicitOrdering``)
- ``UnorderedOrdering`` (providing ``IOrdering``)

If there are custom ``IOrdering`` or ``IExplicitOrdering`` adapters, they must
be tracked accordingly.

There is no ``IOrdering`` adapter for the Plone site root.
An ``IReorderedEvent``-subsciber takes care of tracking first level reorderings.


Development
-----------

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``
6. Shell: ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
-----

- Github: https://github.com/4teamwork/ftw.gopip
- Issues: https://github.com/4teamwork/ftw.gopip/issue
- Pypi: http://pypi.python.org/pypi/ftw.gopip
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.gopip


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.gopip`` is licensed under GNU General Public License, version 2.
