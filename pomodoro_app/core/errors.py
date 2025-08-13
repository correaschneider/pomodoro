class TimerError(Exception):
    """Base class for timer domain errors."""


class InvalidDurationError(TimerError):
    pass


class InvalidStateError(TimerError):
    pass


