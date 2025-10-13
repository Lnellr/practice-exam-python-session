from datetime import datetime

class Task:
    def __init__(self, title, description, priority, due_date, project_id, assignee_id) -> None:
        self.id = None
        self.title = str(title).strip()
        self.description = str(description or "").strip()
        if priority not in (1, 2, 3):
            raise ValueError("priority must be 1, 2 or 3")
        self.priority = priority
        self.status = "pending"
        if due_date is not None and not isinstance(due_date, datetime):
            raise ValueError("due_date must be datetime or None")
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status) -> bool:
        if new_status not in VALID_TASK_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status
        return True

    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return self.status != "completed" and self.due_date < datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "project_id": self.project_id,
            "assignee_id": self.assignee_id,
        }