from dataclasses import dataclass

from typing import Callable, Optional, TypeVar

T = TypeVar("T")

@dataclass

class RetryPolicy:

    """

    Controls how many times an operation may be retried.

    """

    max_retries: int = 2

    def can_retry(self, retry_count: int) -> bool:

        return retry_count < self.max_retries

class RetryManager:

    """

    Executes an operation with bounded retries.

    Retries are intentionally limited so an agent cannot

    repeatedly execute a failing operation indefinitely.

    """

    def __init__(self, policy: Optional[RetryPolicy] = None) -> None:

        self.policy = policy or RetryPolicy()

    def execute(

        self,

        operation: Callable[[], T],

    ) -> tuple[bool, Optional[T], int, Optional[str]]:

        retry_count = 0

        last_error: Optional[str] = None

        while True:

            try:

                result = operation()

                return True, result, retry_count, None

            except Exception as exc:

                last_error = str(exc)

                if not self.policy.can_retry(retry_count):

                    return False, None, retry_count, last_error

                retry_count += 1

