Welcome to the `sphinxcontrib-proof` documentation
==================================================

This `sphinx <http://sphinx.pocoo.org/>`__ extension provides some directives to
typeset theorems, proofs, etc.

Directive list
--------------

Statements
""""""""""

A statement is called using the ``.. proof:theorem`` (replacing `theorem` by
the statement name you want).

Available statements are: `algorithm`, `conjecture`, `definition`, `example`,
`lemma`, `proof`, `property`, `theorem`.

If statement has an argument, it is considered to be the title of the
statement.

Proof
"""""

.. proof:theorem::

    A ``.. proof:proof::`` statement produces a proof.

.. proof:proof::

    This is self-explanatory.


Download and install
--------------------

See the `main project page
<http://git.framasoft.org/spalax/sphinxcontrib-proof>`_ for instructions, and
`changelog
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/master/CHANGELOG.md>`_.

Usage
-----

Add ``sphinxcontrib.proof`` to the list of sphinx extensions in your config
files, and use of the directives provided by this package.

CSS and Javascript
------------------

HTML builder only add some html tags, but does not provides the CSS or
javascript that uses it. You can build your own, or use the one used by this
documentation package (`css
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/master/doc/_static/proof.css>`_
and `javascript
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/master/doc/_static/proof.js>`_)
by placing them into your documentation static directory.

