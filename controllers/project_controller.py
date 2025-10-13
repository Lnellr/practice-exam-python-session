from models.project import Project

class ProjectController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def add_project(self, name, description, start_date, end_date) -> int:
        project = Project(name, description, start_date, end_date)
        return self.db.add_project(project)

    def get_project(self, project_id) -> Project | None:
        return self.db.get_project_by_id(project_id)

    def get_all_projects(self) -> list[Project]:
        return self.db.get_all_projects()

    def update_project(self, project_id, **kwargs) -> bool:
        return self.db.update_project(project_id, **kwargs)

    def delete_project(self, project_id) -> bool:
        return self.db.delete_project(project_id)

    def update_project_status(self, project_id, new_status) -> bool:
        return self.db.update_project(project_id, status=new_status)

    def get_project_progress(self, project_id) -> float:
        project = self.db.get_project_by_id(project_id)
        if not project:
            return 0.0
        # Простая логика: завершён — 100, на паузе — 50, активный — 0
        if project.status == "completed":
            return 100.0
        elif project.status == "on_hold":
            return 50.0
        return 0.0