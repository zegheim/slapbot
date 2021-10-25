import functools
import logging
from typing import Any, Callable, TypeVar, Union, cast

# Allows Pylance / Pyright to display correct tooltip for decorated functions
# See https://github.com/microsoft/pyright/issues/774 for full discussion.
T = TypeVar("T")
_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])


def add_logging(level: Union[int, str] = logging.INFO) -> Callable[[_TFunc], _TFunc]:
    """
    Decorator to inject a logger to the decorated function.
    The logger is named as the decorated function's fully qualified name
    (i.e. in the form of path.to.module.class.function).

    Parameters
    ----------
    level : Union[int, str], optional
        Minimum logging level that the injected logger emits, by default logging.INFO

    Example
    -------
    import logging
    from logging import Logger
    from src.logging import log

    class A:
        @add_logging(level=logging.INFO)
        def my_method(self, logger: Logger) -> None:
            logger.debug("This won't be emitted")
            logger.info("This will be emitted")

    @add_logging(level=logging.DEBUG)
    def my_func(logger: Logger) -> None:
        logger.debug("This will be emitted")

    >>> A().my_method()
    [2021-10-24 14:34:30,079] __main__.A.my_method                  INFO     - This will be emitted
    >>> my_func()
    [2021-10-24 14:34:46,778] __main__.my_func                      DEBUG    - This will be emitted
    """

    def setup_logger(func: _TFunc) -> _TFunc:
        logger = logging.getLogger(f"{func.__module__}.{func.__qualname__}")
        logger.setLevel(level)

        if not len(logger.handlers):
            # logging.getLogger returns the same object each time and
            # we want to make sure we are not adding duplicate handlers
            formatter = logging.Formatter(
                "[{asctime}] {name:<37s} {levelname:<8s} - {message}", style="{"
            )
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        @functools.wraps(func)
        def inject_logger_to_func(*args, **kwargs):
            return func(logger=logger, *args, **kwargs)

        return cast(_TFunc, inject_logger_to_func)

    return setup_logger
