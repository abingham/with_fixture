import tempfile

from with_fixture.testcase import TestCase


class Tracker:
    def __init__(self):
        self.events = []

    def __enter__(self):
        self.events.append('enter')
        return self

    def __exit__(self, t, v, tb):
        self.events.append('exit')


class TestPreYieldIsExecuted(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counter = 0

    @classmethod
    def tearDownClass(cls):
        assert(cls.counter == 1)

    def withFixture(self):
        type(self).counter += 1
        yield

    def test_nothing(self):
        pass


class TestPostYieldIsExecuted(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counter = 0

    @classmethod
    def tearDownClass(cls):
        assert(cls.counter == 1)

    def withFixture(self):
        yield
        type(self).counter += 1

    def test_nothing(self):
        pass


class TestContextManagerBehavior(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tracker = Tracker()

    @classmethod
    def tearDownClass(cls):
        assert(cls.tracker.events == ['enter', 'exit'])

    def withFixture(self):
        with self.tracker:
            yield

    def test_nothing(self):
        pass


class TestBindingToMembers(TestCase):
    TEST_DATA = b'1234567890'

    def withFixture(self):
        with tempfile.TemporaryFile() as self.f:
            yield
            self.f.seek(0)
            assert(self.f.read() == self.TEST_DATA)

    def test_nothing(self):
        self.f.write(self.TEST_DATA)
