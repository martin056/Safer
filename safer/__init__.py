from .factory import SaferFactory
from .exceptions import *  # noqa


Safer = SaferFactory.create


class WithSafer:
    def setUp(self):
        self._safer = Safer()
        super().setUp()

    def tearDown(self):
        self._safer.__cache__ = {}
        super().tearDown()
