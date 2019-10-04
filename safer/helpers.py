from contextlib import contextmanager

from .modes import SaferModes


class SaferHelpers:
    def __init__(self, faker):
        self.faker = faker

    def set_up(self):
        self.faker.turn_off = self.turn_off
        self.faker.insecure = self.insecure
        self.faker.toughen_up = self.toughen_up

    def turn_off(self):
        self.faker._safe_mode = SaferModes.OFF

    @contextmanager
    def insecure(self):
        curr_mode = getattr(self.faker, '_safe_mode', SaferModes.SAFE)
        self.turn_off()
        yield
        self.faker._safe_mode = curr_mode

    @contextmanager
    def toughen_up(self):
        curr_mode = getattr(self.faker, '_safe_mode', SaferModes.SAFE)
        self.faker._safe_mode = SaferModes.STRICT
        yield
        self.faker._safe_mode = curr_mode
