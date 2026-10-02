from dataclasses import dataclass, field

from datetime import datetime

from typing import List, Optional

@dataclass

class WorkflowMetrics:

    """

    Reliability metrics collected during workflow execution.

    """

    workflow_id: str

    started_at: datetime = field(default_factory=datetime.utcnow)

    completed_at: Optional[datetime] = None

    total_tasks: int = 0

    successful_tasks: int = 0

    failed_tasks: int = 0

    retry_count: int = 0

    rollback_count: int = 0

    safe_stop_count: int = 0

    def record_success(self) -> None:

        self.successful_tasks += 1

    def record_failure(self) -> None:

        self.failed_tasks += 1

    def record_retry(self) -> None:

        self.retry_count += 1

    def record_rollback(self) -> None:

        self.rollback_count += 1

    def record_safe_stop(self) -> None:

        self.safe_stop_count += 1

    def complete(self) -> None:

        self.completed_at = datetime.utcnow()

    @property

    def success_rate(self) -> float:

        if self.total_tasks == 0:

            return 0.0

        return self.successful_tasks / self.total_tasks

    @property

    def end_to_end_latency_seconds(self) -> Optional[float]:

        if self.completed_at is None:

            return None

        return (

            self.completed_at - self.started_at

        ).total_seconds()

class MetricsCollector:

    """

    Collects metrics for multiple workflow executions.

    """

    def __init__(self) -> None:

        self.workflows: List[WorkflowMetrics] = []

    def start_workflow(

        self,

        workflow_id: str,

        total_tasks: int,

    ) -> WorkflowMetrics:

        metrics = WorkflowMetrics(

            workflow_id=workflow_id,

            total_tasks=total_tasks,

        )

        self.workflows.append(metrics)

        return metrics

    def get_workflow(

        self,

        workflow_id: str,

    ) -> WorkflowMetrics:

        for workflow in self.workflows:

            if workflow.workflow_id == workflow_id:

                return workflow

        raise KeyError(

            f"Workflow metrics not found: {workflow_id}"

        )

    def calculate_mttr(self) -> Optional[float]:

        """

        Calculate average workflow recovery time.

        For this prototype, workflow duration is used as the

        recovery interval. A production implementation would

        record explicit incident and recovery timestamps.

        """

        completed = [

            workflow.end_to_end_latency_seconds

            for workflow in self.workflows

            if workflow.end_to_end_latency_seconds is not None

        ]

        if not completed:

            return None

        return sum(completed) / len(completed)
