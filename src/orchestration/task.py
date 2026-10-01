from dataclasses import dataclass, field

from enum import Enum

from typing import Any, Dict, List

class TaskStatus(str, Enum):

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    PASSED = "PASSED"

    FAILED = "FAILED"

    BLOCKED = "BLOCKED"

    SKIPPED = "SKIPPED"

    ROLLED_BACK = "ROLLED_BACK"

@dataclass

class Task:

    task_id: str

    name: str

    description: str

    dependencies: List[str] = field(default_factory=list)

    status: TaskStatus = TaskStatus.PENDING

    retry_count: int = 0

    max_retries: int = 2

    input_context: Dict[str, Any] = field(default_factory=dict)

    output: Dict[str, Any] = field(default_factory=dict)

    requires_human_approval: bool = False

    def can_run(self, completed_tasks: set[str]) -> bool:

        """

        A task can run only when all dependencies are completed.

        """

        return all(

            dependency in completed_tasks

            for dependency in self.dependencies

        )

    def mark_running(self) -> None:

        self.status = TaskStatus.RUNNING

    def mark_passed(self, output: Dict[str, Any] | None = None) -> None:

        self.status = TaskStatus.PASSED

        if output:

            self.output = output

    def mark_failed(self) -> None:

        self.status = TaskStatus.FAILED

    def mark_rolled_back(self) -> None:

        self.status = TaskStatus.ROLLED_BACK

    def can_retry(self) -> bool:

        return self.retry_count < self.max_retries

    def increment_retry(self) -> None:

        self.retry_count += 1

