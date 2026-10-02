from dataclasses import dataclass

from enum import Enum

from typing import Optional

class GateStatus(str, Enum):

    PENDING = "PENDING"

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"

    BLOCKED = "BLOCKED"

@dataclass

class ApprovalGate:

    gate_id: str

    name: str

    description: str

    requires_human_approval: bool = True

    status: GateStatus = GateStatus.PENDING

    approved_by: Optional[str] = None

    rejection_reason: Optional[str] = None

    def approve(self, approved_by: str) -> None:

        if not approved_by:

            raise ValueError("Approver identity is required.")

        self.status = GateStatus.APPROVED

        self.approved_by = approved_by

        self.rejection_reason = None

    def reject(self, reason: str) -> None:

        if not reason:

            raise ValueError("Rejection reason is required.")

        self.status = GateStatus.REJECTED

        self.rejection_reason = reason

    def block(self) -> None:

        self.status = GateStatus.BLOCKED

    def is_open(self) -> bool:

        return self.status == GateStatus.APPROVED

class GateManager:

    """

    Controls workflow entry and exit gates.

    """

    def __init__(self) -> None:

        self.gates: dict[str, ApprovalGate] = {}

    def add_gate(self, gate: ApprovalGate) -> None:

        if gate.gate_id in self.gates:

            raise ValueError(f"Gate already exists: {gate.gate_id}")

        self.gates[gate.gate_id] = gate

    def approve_gate(

        self,

        gate_id: str,

        approved_by: str,

    ) -> None:

        gate = self._get_gate(gate_id)

        gate.approve(approved_by)

    def reject_gate(

        self,

        gate_id: str,

        reason: str,

    ) -> None:

        gate = self._get_gate(gate_id)

        gate.reject(reason)

    def is_approved(self, gate_id: str) -> bool:

        return self._get_gate(gate_id).is_open()

    def _get_gate(self, gate_id: str) -> ApprovalGate:

        if gate_id not in self.gates:

            raise KeyError(f"Gate not found: {gate_id}")

        return self.gates[gate_id]
