# Safer
Experimental Faker extension that is safer and is less likely to generate duplicate values in a single test run.

## The Idea

[Faker](https://github.com/joke2k/faker) is great. We love using it in our Python and Django unit tests.

The problem with it is that it does not have that **big data corpus** and the **uniqueness** of the generated values is not ensured. This makes some of our CI builds to fail randomnly. There are several approaches to solve this and the solution is up to you.

**Safer** takes the caching approach to deal with these problems. It makes sure the generated values are not repeated. We allow the user to switch on and off this behaviour.

### API

**Safer** has all of the Faker's providers so you can use it API with no problem.

Basically, all you need is to instantiate from the base Safer class:
```
from safer import Safer

safer = Safer()
```

There is on mixin called `WithSafer` and we recommend using it in your unit tests:
```
from unittest import TestCase
from safer import WithSafer

class ExampleTests(WithSafer, TestCase):
    pass
```
**NOTE: If you don't use it, you need to take care of the `smarter.__cache__` yourself!**

If you want to use Safer but you don't want its main functionallity you can turn it off using the `insecure` context manager:
```
from safer import Safer

safer = Safer()
with safer.insecure():
    name = safer.name()
```

If you want to raise an error every time a non-unique value is generated you can use the `toughen_up` context manager:
```
from safer import Safer

safer = Safer()
with safer.toughen_up():
    name = safer.name()
```
It will raise a `ValueAlreadyGeneratedError` exception.

If Safer is not able to generate a unique value a `CannotGenerateUniqueValueError` will be raised.