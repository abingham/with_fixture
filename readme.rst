`Travis CI <https://travis-ci.org/abingham/with_fixture>`_ |build-status|
`Landscape.io <https://landscape.io/github/abingham/with_fixture>`_ |code-health|

================
 with_fixture
================

``with_fixture`` is an experiment in using context-managers naturally
with Python ``unittest`` fixtures.

Test fixtures and context-managers have very similar structures. In
both cases, they define bits of code to be run before and after other
bits of *a priori* unknown code. They are the bread in little code
sandwiches.

Yet, as far as I know, there is no natural way to use them
together. That is, there is no way to use context-managers in (or
perhaps *as*) test fixtures with the standard ``unittest`` module. This
is doubly egregious because context-managers are a central element in
modern Python design, and we should be encouraging their use widely.

``with_fixture``, then, is an experiment in making them work together. I
want to start to explore the options we have for using
context-managers in test fixtures, with the long-term goal of getting
something into the standard library.

Experiment 1: ``with_fixture.TestCase.withFixture()``
=====================================================

``with_fixture`` currently implements a single, simple approach to
combining context-managers and fixtures; it's a kind of minimum
viable product. The idea is to subclass ``unittest.TestCase`` and
override the ``setUp()`` and ``tearDown()`` methods to drive a new
generator method, ``withFixture()``.

``withFixture()`` must call ``yield`` once. Everything before the ``yield``
is the equivalent of ``setUp()`` in ``unittest.TestCase``, and everything
after the ``yield`` is equivalent to ``tearDown()``. By placing the
``yield`` in a *with-block*, it becomes very natural to use
context-managers in test fixtures.

Example: Temporary file
-----------------------

Here we use the ``tempfile.TemporaryFile`` context-manager in ``withFixture()``::

  import with_fixture

  class TestBindingToMembers(with_fixture.TestCase):
      TEST_DATA = b'1234567890'

      def withFixture(self):
          # This creates a tempfile and binds it to self.f
          with tempfile.TemporaryFile() as self.f:
              # This yield sends control to the test
              yield

              # The test has now been executed. Check for the data we
              # expect in the file.
              self.f.seek(0)
              assert(self.f.read() == self.TEST_DATA)

      def test_nothing(self):
          self.f.write(self.TEST_DATA)

This is clearly a bit contrived (it's taken from the somewhat awkward
test suite for ``with_fixture`` itself), but you can see what's going
on.

Future work
===========

The current implementation is small and simple, and there's plenty of
room for further experimentation. Areas to investigate include:

 - Allowing users to use ``setUp()`` and ``tearDown()`` along with
   ``withFixture()``. Currently we make that difficult. There are a
   number of interesting problems that arise when you start to think
   about this.

 - Integrating an implementation directly into ``unittest``.

 - Consider alternative names. I think ``withFixture`` is pretty good
   and communicates the design intent, but others may find it
   confusing.

 - Consider equivalent support for ``setUp/tearDownClass()``.

 - Do some deeper thinking on exceptions. I *think* the currently
   implementation is pretty sound WRT exceptions (i.e. that setup and
   teardown will get executed correctly in the face of exceptions) but
   I'm not testing it and haven't given it great throught yet.

 - Completely different designs. I can imagine completely different
   ways to approach this, and I'm sure others can too.

.. Build status badge
.. |build-status|
   image:: https://secure.travis-ci.org/abingham/with_fixture.png
           ?branch=master
   :target: http://travis-ci.org/abingham/with_fixture
   :alt: Build status

.. Landscape health badge
.. |code-health|
   image:: https://landscape.io/github/abingham/with_fixture/master/badges
   :target: https://landscape.io/github/abingham/with_fixture
   :alt: Code health
