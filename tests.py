from unittest import TestCase
from safer import WithSafer, ValueAlreadyGeneratedError


class ExampleTests(WithSafer, TestCase):
    def test_with_strict_safer(self):
        i = 1
        with self._safer.toughen_up():
            while True:
                try:
                    self._safer.name()

                    i += 1

                    if i == 10000:
                        break

                except ValueAlreadyGeneratedError as exc:
                    print(f'Got duplicate value at {i} iterration.')
                    print(f'The exception was: {exc}')
                    break

    def test_safer_name_does_generates_unique_values(self):
        i = 1
        while True:
            self._safer.name()

            i += 1

            if i == 10000:
                print('Did not generate duplicate value after 10K iterrations')
                break
