from datetime import datetime

class Project:
    def __init__(self, name, description, start_date, end_date) -> None:
        self.id = None
        self.name = str(name).strip()
        self.description = str(description or "").strip()
        if start_date is not None and not isinstance(start_date, datetime):
            raise ValueError("start_date must be datetime or None")
        if end_date is not None and not isinstance(end_date, datetime):
            raise ValueError("end_date must be datetime or None")
        self.start_date = start_date
        self.end_date = end_date
        self.status = "active"

    def update_status(self, new_status) -> bool:
        if new_status not in VALID_PROJECT_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status
        return True

    def get_progress(self) -> float:
        if self.status == "completed":
            return 100
        if self.status == "on_hold":
            return 50
        if self.end_date and datetime.now() > self.end_date:
            return 100
        return 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
        }