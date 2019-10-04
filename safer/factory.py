from faker.factory import Factory

from .modes import SaferModes
from .helpers import SaferHelpers
from .utils import is_provider_method, ensure_faker_method


class SaferFactory(Factory):
    DEFFAULT_MODE = SaferModes.SAFE

    @classmethod
    def create(cls, *args, **kwargs):
        faker = super(SaferFactory, cls).create(*args, **kwargs)
        faker.__cache__ = {}
        faker._safe_mode = cls.DEFFAULT_MODE

        for method in faker.__dict__.values():
            if is_provider_method(method):
                faker.__cache__[method.__name__] = []
                setattr(faker, method.__name__, ensure_faker_method(faker, method))

        # *NOTE*: This should not be done like this!
        # TODO: Debug why creating new Generator does not work!
        faker_helpers = SaferHelpers(faker)
        faker_helpers.set_up()

        return faker
