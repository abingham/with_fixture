import unittest


class TestCase(unittest.TestCase):
    def withFixture(self):
        yield

    def setUp(self):
        self._fixture_iter = iter(self.withFixture())
        next(self._fixture_iter)

    def tearDown(self):
        try:
            next(self._fixture_iter)
        except StopIteration:
            pass
