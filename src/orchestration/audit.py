from dataclasses import asdict, dataclass

from datetime import datetime

from typing import Any, Dict, List, Optional

@dataclass

class AuditEvent:

    """

    Immutable-style record of an important workflow event.

    """

    event_type: str

    workflow_id: str

    task_id: Optional[str]

    agent: Optional[str]

    action: str

    result: str

    details: Dict[str, Any]

    timestamp: str

class AuditLogger:

    """

    Stores an audit trail for workflow execution.

    In a production system this could write to a centralized

    logging or event-streaming platform.

    """

    def __init__(self) -> None:

        self.events: List[AuditEvent] = []

    def record(

        self,

        event_type: str,

        workflow_id: str,

        action: str,

        result: str,

        task_id: Optional[str] = None,

        agent: Optional[str] = None,

        details: Optional[Dict[str, Any]] = None,

    ) -> AuditEvent:

        event = AuditEvent(

            event_type=event_type,

            workflow_id=workflow_id,

            task_id=task_id,

            agent=agent,

            action=action,

            result=result,

            details=details or {},

            timestamp=datetime.utcnow().isoformat(),

        )

        self.events.append(event)

        return event

    def get_events(

        self,

        workflow_id: Optional[str] = None,

    ) -> List[AuditEvent]:

        if workflow_id is None:

            return list(self.events)

        return [

            event

            for event in self.events

            if event.workflow_id == workflow_id

        ]

    def export(self) -> List[Dict[str, Any]]:

        return [asdict(event) for event in self.events]

