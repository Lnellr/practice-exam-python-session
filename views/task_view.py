import tkinter as tk
from tkinter import ttk, messagebox

class TaskView(ttk.Frame):
    def __init__(self, parent, task_controller, project_controller, user_controller) -> None:
        super().__init__(parent)
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self) -> None:
        # ----- Форма добавления задачи -----
        form = ttk.LabelFrame(self, text="Добавить задачу")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.e_title = ttk.Entry(form)
        self.e_title.grid(row=0, column=1, sticky="ew", padx=5, pady=4)

        ttk.Label(form, text="Описание:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.e_desc = ttk.Entry(form)
        self.e_desc.grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        ttk.Label(form, text="Приоритет (1/2/3):").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.e_priority = ttk.Entry(form)
        self.e_priority.insert(0, "2")
        self.e_priority.grid(row=2, column=1, sticky="ew", padx=5, pady=4)

        ttk.Label(form, text="Срок (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=5, pady=4)
        self.e_due = ttk.Entry(form)
        self.e_due.grid(row=3, column=1, sticky="ew", padx=5, pady=4)

        ttk.Label(form, text="ID проекта:").grid(row=4, column=0, sticky="w", padx=5, pady=4)
        self.e_project = ttk.Entry(form)
        self.e_project.grid(row=4, column=1, sticky="ew", padx=5, pady=4)

        ttk.Label(form, text="ID исполнителя:").grid(row=5, column=0, sticky="w", padx=5, pady=4)
        self.e_assignee = ttk.Entry(form)
        self.e_assignee.grid(row=5, column=1, sticky="ew", padx=5, pady=4)

        btn_add = ttk.Button(form, text="Добавить", command=self.add_task)
        btn_add.grid(row=6, column=0, columnspan=2, pady=8)

        form.columnconfigure(1, weight=1)

        # ----- Таблица задач -----
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id","title","status","priority","due_date","project_id","assignee_id"),
            show="headings"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название")
        self.tree.heading("status", text="Статус")
        self.tree.heading("priority", text="Приоритет")
        self.tree.heading("due_date", text="Срок")
        self.tree.heading("project_id", text="Проект")
        self.tree.heading("assignee_id", text="Исполнитель")

        self.tree.column("id", width=60)
        self.tree.column("title", width=220)
        self.tree.column("status", width=110)
        self.tree.column("priority", width=90)
        self.tree.column("due_date", width=120)
        self.tree.column("project_id", width=90)
        self.tree.column("assignee_id", width=110)

        self.tree.pack(fill="both", expand=True, side="left")

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        # ----- Кнопки управления -----
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=10, pady=5)
        ttk.Button(bar, text="Обновить список", command=self.refresh_tasks).pack(side="left", padx=5)
        ttk.Button(bar, text="Удалить выбранную", command=self.delete_selected).pack(side="left", padx=5)

    def refresh_tasks(self) -> None:
        # очистка
        for i in self.tree.get_children():
            self.tree.delete(i)
        # получение задач (ожидаем модели Task)
        tasks = self.task_controller.get_all_tasks()
        for t in tasks:
            # поддержка как моделей с атрибутами, так и dict-подобных (на всякий случай)
            get = (lambda obj, name: getattr(obj, name) if hasattr(obj, name) else obj.get(name))
            tid = get(t, "id")
            title = get(t, "title")
            status = get(t, "status")
            priority = get(t, "priority")
            due = get(t, "due_date")
            # due может быть datetime или строка
            if hasattr(due, "isoformat"):
                due = due.isoformat()
            project_id = get(t, "project_id")
            assignee_id = get(t, "assignee_id")
            self.tree.insert("", "end", values=(tid, title, status, priority, due, project_id, assignee_id))

    def add_task(self) -> None:
        title = self.e_title.get().strip()
        desc = self.e_desc.get().strip()
        prio_raw = self.e_priority.get().strip()
        due_raw = self.e_due.get().strip()
        proj_raw = self.e_project.get().strip()
        ass_raw = self.e_assignee.get().strip()

        if not title:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")
            return

        # priority
        try:
            priority = int(prio_raw) if prio_raw else 2
        except ValueError:
            messagebox.showerror("Ошибка", "Приоритет должен быть числом 1, 2 или 3.")
            return

        # due_date (без добавления import — используем __import__)
        due_dt = None
        if due_raw:
            try:
                dtm = __import__('datetime')
                due_dt = dtm.datetime.fromisoformat(due_raw)
            except Exception:
                messagebox.showerror("Ошибка", "Срок должен быть в формате YYYY-MM-DD.")
                return

        project_id = int(proj_raw) if proj_raw else None
        assignee_id = int(ass_raw) if ass_raw else None

        try:
            self.task_controller.add_task(title, desc, priority, due_dt, project_id, assignee_id)
            messagebox.showinfo("Успех", "Задача добавлена.")
            self.refresh_tasks()
            # очистка полей
            for e in (self.e_title, self.e_desc, self.e_priority, self.e_due, self.e_project, self.e_assignee):
                e.delete(0, tk.END)
            self.e_priority.insert(0, "2")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_selected(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Внимание", "Выберите задачу для удаления.")
            return
        task_id = self.tree.item(sel[0])["values"][0]
        try:
            self.task_controller.delete_task(task_id)
            messagebox.showinfo("Успех", "Задача удалена.")
            self.refresh_tasks()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))