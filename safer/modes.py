from enum import Enum


class SaferModes(Enum):
    SAFE = 'SAFE'
    WARNING = 'warning'
    STRICT = 'strict'
    OFF = 'off'
