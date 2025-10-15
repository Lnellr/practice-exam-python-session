import sqlite3
from models.task import Task
from models.project import Project
from models.user import User
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="tasks.db") -> None:
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def close(self) -> None:
        self.conn.close()

    def create_tables(self) -> None:
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT,
            project_id INTEGER NOT NULL,
            assignee_id INTEGER NOT NULL
            -- внешние ключи по желанию
);
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT NOT NULL
);
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            registration_date TEXT NOT NULL
);
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status  ON tasks(status);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due     ON tasks(due_date);")
        self.conn.commit()

    def add_task(self, task: Task) -> int:
        cur = self.conn.execute(
        "INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            task.title,
            task.description,
            int(task.priority),
            task.status,
            task.due_date.isoformat() if task.due_date else None,
            int(task.project_id),
            int(task.assignee_id),
        ),
    )
        self.conn.commit()
        return cur.lastrowid


    def get_task_by_id(self, task_id) -> Task | None:
        r = self.conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not r:
            return None
        from models.task import Task
        from datetime import datetime
        due = datetime.fromisoformat(r["due_date"]) if r["due_date"] else None
        t = Task(r["title"], r["description"], r["priority"], due, r["project_id"], r["assignee_id"])
        t.id = r["id"]
        t.status = r["status"]
        return t

    def get_all_tasks(self) -> list[Task]:
        rows = self.conn.execute(
            "SELECT id, title, description, priority, status, due_date, project_id, assignee_id "
            "FROM tasks ORDER BY id"
        ).fetchall()
        from models.task import Task
        from datetime import datetime

        out: list[Task] = []
        for r in rows:
            due = datetime.fromisoformat(r["due_date"]) if r["due_date"] else None
            t = Task(r["title"], r["description"], r["priority"], due, r["project_id"], r["assignee_id"])
            t.id = r["id"]
            t.status = r["status"]
            out.append(t)
        return out

    def update_task(self, task_id, **kwargs) -> bool:
        if not kwargs:
            return False
        cols, params = [], []
        for k, v in kwargs.items():
            if isinstance(v, datetime):
                v = v.isoformat()
            cols.append(f"{k}=?")
            params.append(v)
        params.append(task_id)
        self.conn.execute(f"UPDATE tasks SET {', '.join(cols)} WHERE id=?", params)
        self.conn.commit()
        return True

    def delete_task(self, task_id) -> bool:
        self.conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()
        return True

    def search_tasks(self, query) -> list[Task]:
        q = f"%{str(query).strip()}%"
        rows = self.conn.execute(
        "SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ? ORDER BY id", (q, q)
    ).fetchall()
        from models.task import Task
        from datetime import datetime
        out = []
        for r in rows:
            due = datetime.fromisoformat(r["due_date"]) if r["due_date"] else None
            t = Task(r["title"], r["description"], r["priority"], due, r["project_id"], r["assignee_id"])
            t.id = r["id"]; t.status = r["status"]
            out.append(t)
        return out

    def get_tasks_by_project(self, project_id) -> list[Task]:
        rows = self.conn.execute(
        "SELECT * FROM tasks WHERE project_id=? ORDER BY id", (project_id,)
        ).fetchall()
        from models.task import Task
        from datetime import datetime
        out = []
        for r in rows:
            due = datetime.fromisoformat(r["due_date"]) if r["due_date"] else None
        t = Task(r["title"], r["description"], r["priority"], due, r["project_id"], r["assignee_id"])
        t.id = r["id"]; t.status = r["status"]
        out.append(t)
        return out


    def get_tasks_by_user(self, user_id) -> list[Task]:
        rows = self.conn.execute(
            "SELECT id, title, description, priority, status, due_date, project_id, assignee_id "
            "FROM tasks WHERE assignee_id=? ORDER BY id",
        (user_id,),
        ).fetchall()
        from models.task import Task
        from datetime import datetime
        out = []
        for r in rows:
            due = datetime.fromisoformat(r["due_date"]) if r["due_date"] else None
            t = Task(r["title"], r["description"], r["priority"], due, r["project_id"], r["assignee_id"])
            t.id = r["id"]; t.status = r["status"]
            out.append(t)
        return out

    def add_project(self, project: Project) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO projects(name, description, start_date, end_date, status) VALUES(?,?,?,?,?)",
            (
                project.name,
                project.description,
                project.start_date.isoformat() if project.start_date else None,
                project.end_date.isoformat() if project.end_date else None,
                project.status,
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_project_by_id(self, project_id) -> Project | None:
        r = self.conn.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()
        if not r:
            return None
        from models.project import Project
        from datetime import datetime
        start = datetime.fromisoformat(r["start_date"]) if r["start_date"] else None
        end = datetime.fromisoformat(r["end_date"]) if r["end_date"] else None
        p = Project(r["name"], r["description"], start, end)
        p.id = r["id"]; p.status = r["status"]
        return p
    def get_all_projects(self) -> list[Project]:
        rows = self.conn.execute("SELECT * FROM projects ORDER BY id").fetchall()
        from models.project import Project
        from datetime import datetime
        out = []
        for r in rows:
            start = datetime.fromisoformat(r["start_date"]) if r["start_date"] else None
            end = datetime.fromisoformat(r["end_date"]) if r["end_date"] else None
            p = Project(r["name"], r["description"], start, end)
            p.id = r["id"]; p.status = r["status"]
            out.append(p)
        return out

    def update_project(self, project_id, **kwargs) -> bool:
        if not kwargs:
            return False
        cols, params = [], []
        for k, v in kwargs.items():
            if isinstance(v, datetime):
                v = v.isoformat()
            cols.append(f"{k}=?")
            params.append(v)
        params.append(project_id)
        self.conn.execute(f"UPDATE projects SET {', '.join(cols)} WHERE id=?", params)
        self.conn.commit()
        return True

    def delete_project(self, project_id) -> bool:
        self.conn.execute("DELETE FROM projects WHERE id=?", (project_id,))
        self.conn.commit()
        return True

    def add_user(self, user: User) -> int:
        cur = self.conn.execute(
        "INSERT INTO users (username, email, role, registration_date) "
        "VALUES (?, ?, ?, ?)",
        (user.username, user.email, user.role, user.registration_date.isoformat()),
    )
        self.conn.commit()
        return cur.lastrowid

    def get_user_by_id(self, user_id) -> User | None:
        r = self.conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if not r:
            return None
        from models.user import User
        from datetime import datetime
        u = User(r["username"], r["email"], r["role"])
        u.id = r["id"]
        u.registration_date = datetime.fromisoformat(r["registration_date"])
        return u

    def get_all_users(self) -> list[User]:
        rows = self.conn.execute(
            "SELECT id, username, email, role, registration_date FROM users ORDER BY id"
        ).fetchall()
        from models.user import User
        from datetime import datetime

        out: list[User] = []
        for r in rows:
            u = User(r["username"], r["email"], r["role"])
            u.id = r["id"]
            u.registration_date = datetime.fromisoformat(r["registration_date"])
            out.append(u)
        return out

    def update_user(self, user_id, **kwargs) -> bool:
        if not kwargs:
            return False
        cols, params = [], []
        for k, v in kwargs.items():
            cols.append(f"{k}=?")
            params.append(v)
        params.append(user_id)
        self.conn.execute(f"UPDATE users SET {', '.join(cols)} WHERE id=?", params)
        self.conn.commit()
        return True

    def delete_user(self, user_id) -> bool:
        self.conn.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()
        return True
    #ggjri