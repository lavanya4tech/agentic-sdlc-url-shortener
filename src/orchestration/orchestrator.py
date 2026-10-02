from typing import Callable, Dict, List, Optional

from .audit import AuditLogger

from .gates import GateManager

from .graph import DependencyGraph

from .metrics import MetricsCollector

from .retry import RetryManager

from .rollback import RollbackManager, SafeStopController

from .state import WorkflowState

from .task import Task, TaskStatus

class Orchestrator:

    """

    Coordinates the end-to-end SDLC workflow.

    Responsibilities:

    - Dependency-aware task execution

    - Human approval gates

    - Bounded retries

    - Rollback and safe-stop

    - Audit logging

    - Reliability metrics

    """

    def __init__(

        self,

        workflow_id: str,

        requirement: str,

    ) -> None:

        self.workflow_id = workflow_id

        self.state = WorkflowState(

            workflow_id=workflow_id,

            requirement=requirement,

        )

        self.graph = DependencyGraph()

        self.gates = GateManager()

        self.retry_manager = RetryManager()

        self.rollback_manager = RollbackManager()

        self.safe_stop = SafeStopController()

        self.audit = AuditLogger()

        self.metrics = MetricsCollector()

        self.task_handlers: Dict[str, Callable[[], Dict]] = {}

    def add_task(

        self,

        task: Task,

        handler: Callable[[], Dict],

    ) -> None:

        self.graph.add_task(task)

        self.task_handlers[task.task_id] = handler

    def add_gate(self, gate) -> None:

        self.gates.add_gate(gate)

    def validate_workflow(self) -> None:

        """

        Validate dependencies before execution.

        """

        self.graph.validate()

        self.audit.record(

            event_type="WORKFLOW_VALIDATION",

            workflow_id=self.workflow_id,

            action="validate_workflow",

            result="PASSED",

        )

    def execute(self) -> WorkflowState:

        """

        Execute tasks while respecting dependencies,

        gates, retries, and safe-stop controls.

        """

        self.validate_workflow()

        total_tasks = len(self.graph.get_all_tasks())

        workflow_metrics = self.metrics.start_workflow(

            workflow_id=self.workflow_id,

            total_tasks=total_tasks,

        )

        self.state.status = "RUNNING"

        while True:

            if self.safe_stop.is_stopped():

                self.state.request_safe_stop(

                    self.safe_stop.reason or "Unknown reason"

                )

                break

            completed = set(self.state.completed_tasks)

            ready_tasks = self.graph.get_ready_tasks(

                completed

            )

            if not ready_tasks:

                break

            progress_made = False

            for task in ready_tasks:

                if task.requires_human_approval:

                    gate_id = f"{task.task_id}_gate"

                    if not self.gates.is_approved(gate_id):

                        task.status = TaskStatus.BLOCKED

                        self.audit.record(

                            event_type="APPROVAL_REQUIRED",

                            workflow_id=self.workflow_id,

                            task_id=task.task_id,

                            agent="orchestrator",

                            action="human_approval",

                            result="BLOCKED",

                        )

                        continue

                handler = self.task_handlers.get(

                    task.task_id

                )

                if handler is None:

                    task.mark_failed()

                    self.state.mark_failed(

                        task.task_id

                    )

                    self.audit.record(

                        event_type="TASK_FAILED",

                        workflow_id=self.workflow_id,

                        task_id=task.task_id,

                        agent="orchestrator",

                        action="execute_task",

                        result="NO_HANDLER",

                    )

                    workflow_metrics.record_failure()

                    continue

                task.mark_running()

                self.audit.record(

                    event_type="TASK_STARTED",

                    workflow_id=self.workflow_id,

                    task_id=task.task_id,

                    agent=task.name,

                    action="execute",

                    result="STARTED",

                )

                success, result, retries, error = (

                    self.retry_manager.execute(handler)

                )

                for _ in range(retries):

                    workflow_metrics.record_retry()

                if success:

                    task.mark_passed(

                        result or {}

                    )

                    self.state.mark_completed(

                        task.task_id

                    )

                    self.state.add_audit_event(

                        event="TASK_COMPLETED",

                        task_id=task.task_id,

                        details=result or {},

                    )

                    workflow_metrics.record_success()

                    self.audit.record(

                        event_type="TASK_COMPLETED",

                        workflow_id=self.workflow_id,

                        task_id=task.task_id,

                        agent=task.name,
