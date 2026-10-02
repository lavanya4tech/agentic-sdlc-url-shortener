from dataclasses import dataclass, field

from typing import Callable, List, Optional

@dataclass

class RollbackAction:

    """

    Represents one reversible action performed during a workflow.

    """

    action_id: str

    description: str

    rollback: Callable[[], None]

@dataclass

class RollbackManager:

    """

    Maintains reversible actions and executes them in reverse order

    when rollback is required.

    """

    actions: List[RollbackAction] = field(default_factory=list)

    def register(

        self,

        action_id: str,

        description: str,

        rollback: Callable[[], None],

    ) -> None:

        self.actions.append(

            RollbackAction(

                action_id=action_id,

                description=description,

                rollback=rollback,

            )

        )

    def execute(self) -> List[str]:

        """

        Execute registered rollback actions in reverse order.

        """

        completed: List[str] = []

        for action in reversed(self.actions):

            action.rollback()

            completed.append(action.action_id)

        self.actions.clear()

        return completed

class SafeStopController:

    """

    Prevents additional workflow execution when a critical

    condition is detected.

    """

    def __init__(self) -> None:

        self.stopped = False

        self.reason: Optional[str] = None

    def stop(self, reason: str) -> None:

        if not reason:

            raise ValueError("Safe-stop reason is required.")

        self.stopped = True

        self.reason = reason

    def reset(self) -> None:

        self.stopped = False

        self.reason = None

    def is_stopped(self) -> bool:

        return self.stopped

