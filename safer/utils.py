import inspect
from functools import wraps

from faker.providers import BaseProvider

from .modes import SaferModes
from .exceptions import ValueAlreadyGeneratedError, CannotGenerateUniqueValueError


def is_provider_method(method):
    return callable(method) and\
        not method.__name__.startswith('_Generator__') and\
        hasattr(method, '__self__') and\
        isinstance(method.__self__, BaseProvider)


def get_faker_method_caller(caller_stack):
    if caller_stack[3].frame.f_locals.get('self', None):
        return caller_stack[3].frame.f_locals['self']

    if caller_stack[2].frame.f_locals.get('self', None):
        return caller_stack[2].frame.f_locals['self']

    return None


def ensure_faker_method(faker, faker_method):
    @wraps(faker_method)
    def wrapper(*args, **kwargs):
        result = faker_method(*args, **kwargs)

        # We don't want to cache the methods that Faker uses internally.
        # For example, when someone calls faker.name() -> Faker internally calls
        # faker.first_name + faker.last_name().
        # We will cache only the result from the `faker.name()` call.
        provider_caller = get_faker_method_caller(inspect.stack())

        if provider_caller is not faker and not isinstance(provider_caller, BaseProvider):
            if result in faker.__cache__[faker_method.__name__]:

                faker_mode = getattr(faker, '_safe_mode', None)
                msg = f'{result} from faker\'s `{faker_method.__name__}` was generated already.'

                if faker_mode == SaferModes.OFF:
                    pass

                if faker_mode == SaferModes.SAFE:
                    result = handle_faker_duplicate(
                        curr_result=result,
                        faker=faker,
                        cache=faker.__cache__[faker_method.__name__],
                        method=faker_method,
                        *args,
                        **kwargs
                    )

                if faker_mode == SaferModes.WARNING:
                    print(msg)

                if faker_mode == SaferModes.STRICT:
                    raise ValueAlreadyGeneratedError(msg)

            faker.__cache__[faker_method.__name__].append(result)

        return result

    return wrapper


def handle_faker_duplicate(curr_result, faker, cache, method, *method_args, **method_kwargs):
    result = curr_result
    max_iterrations = 100
    iterration = 1

    with faker.insecure():
        while result in cache:
            if iterration >= max_iterrations:
                raise CannotGenerateUniqueValueError(
                    f'{method.__name__} cannot generate new value for the current run.'
                )

            result = method(*method_args, **method_kwargs)
            iterration += 1

    return result
