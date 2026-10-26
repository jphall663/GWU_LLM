"""Small reusable utilities for the Lecture 3 model-API notebook.

Copyright (c) Patrick Hall (jphall@gwu.edu), 2026--27.
Released under the MIT License.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from time import sleep as default_sleep
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def retry(
    *,
    max_attempts: int,
    base_delay_seconds: float,
    should_retry: Callable[[Exception], bool],
    on_retry: Callable[[int, float, Exception], None] | None = None,
    sleep: Callable[[float], None] = default_sleep,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Return a decorator for a bounded exponential-backoff retry policy.

    The wrapped operation runs at most max_attempts times: O(max_attempts)
    calls and O(1) additional memory. The predicate keeps service failures
    separate from refusals, incomplete outputs, and validation failures.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1.")
    if base_delay_seconds < 0:
        raise ValueError("base_delay_seconds cannot be negative.")

    def decorate(operation: Callable[P, T]) -> Callable[P, T]:
        @wraps(operation)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            for attempt in range(1, max_attempts + 1):
                try:
                    return operation(*args, **kwargs)
                except Exception as error:
                    final_attempt = attempt == max_attempts
                    if final_attempt or not should_retry(error):
                        raise

                    # Exponential backoff is 1x, 2x, 4x, ... the base delay.
                    delay_seconds = base_delay_seconds * (2 ** (attempt - 1))
                    if on_retry is not None:
                        on_retry(attempt, delay_seconds, error)
                    sleep(delay_seconds)

            # Every loop path returns or raises; this line satisfies type checkers.
            raise RuntimeError("Retry loop ended unexpectedly.")

        return wrapped

    return decorate
