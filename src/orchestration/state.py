from dataclasses import dataclass, field

from datetime import datetime

from typing import Any, Dict, List, Optional

@dataclass

class WorkflowState:

    workflow_id: str

    requirement: str

    status: str = "PENDING"

    completed_tasks: List[str] = field(default_factory=list)

    failed_tasks: List[str] = field(default_factory=list)

    context: Dict[str, Any] = field(default_factory=dict)

    decisions: List[Dict[str, Any]] = field(default_factory=list)

    approvals: List[Dict[str, Any]] = field(default_factory=list)

    audit_events: List[Dict[str, Any]] = field(default_factory=list)

    safe_stop: bool = False

    rollback_required: bool = False

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_decision(

        self,

        decision: str,

        rationale: str,

        source: Optional[str] = None,

    ) -> None:

        self.decisions.append(

            {

                "decision": decision,

                "rationale": rationale,

                "source": source,

                "timestamp": datetime.utcnow().isoformat(),

            }

        )

        self.updated_at = datetime.utcnow()

    def add_approval(

        self,

        action: str,

        approved_by: str,

        approved: bool,

    ) -> None:

        self.approvals.append(

            {

                "action": action,

                "approved_by": approved_by,

                "approved": approved,

                "timestamp": datetime.utcnow().isoformat(),

            }

        )

        self.updated_at = datetime.utcnow()

    def add_audit_event(

        self,

        event: str,

        task_id: Optional[str] = None,

        details: Optional[Dict[str, Any]] = None,

    ) -> None:

        self.audit_events.append(

            {

                "event": event,

                "task_id": task_id,

                "details": details or {},

                "timestamp": datetime.utcnow().isoformat(),

            }

        )

        self.updated_at = datetime.utcnow()

    def mark_completed(self, task_id: str) -> None:

        if task_id not in self.completed_tasks:

            self.completed_tasks.append(task_id)

    def mark_failed(self, task_id: str) -> None:

        if task_id not in self.failed_tasks:

            self.failed_tasks.append(task_id)

    def request_safe_stop(self, reason: str) -> None:

        self.safe_stop = True

        self.status = "SAFE_STOP"

        self.add_audit_event(

            event="SAFE_STOP_REQUESTED",

            details={"reason": reason},
}
          
          
          
          
          
      
