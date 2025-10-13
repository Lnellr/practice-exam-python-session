import tkinter as tk
from tkinter import ttk, messagebox

class ProjectView(ttk.Frame):
    def __init__(self, parent, project_controller) -> None:
        super().__init__(parent)
        self.project_controller = project_controller
        self.create_widgets()
        self.refresh_projects()

    def create_widgets(self) -> None:
        form_frame = ttk.LabelFrame(self, text="Добавить проект")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_frame, text="Описание:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Button(form_frame, text="Добавить", command=self.add_project).grid(row=2, column=0, columnspan=2, pady=10)

        form_frame.columnconfigure(1, weight=1)

        # --- таблица проектов ---
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("id", "name", "description", "status"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название")
        self.tree.heading("description", text="Описание")
        self.tree.heading("status", text="Статус")

        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("description", width=300)
        self.tree.column("status", width=100)

        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # --- кнопки управления ---
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="Обновить список", command=self.refresh_projects).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Удалить выбранный", command=self.delete_selected).pack(side="left", padx=5)

    def refresh_projects(self) -> None:
        # Очистить таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Получить все проекты и отобразить
        projects = self.project_controller.get_all_projects()
        for project in projects:
            self.tree.insert("", "end", values=(project.id, project.name, project.description, project.status))

    def add_project(self) -> None:
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "Название проекта не может быть пустым!")
            return

        self.project_controller.add_project(name, desc, None, None)
        messagebox.showinfo("Успех", "Проект добавлен!")
        self.refresh_projects()
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Сначала выберите проект для удаления.")
            return

        project_id = self.tree.item(selected[0])["values"][0]
        self.project_controller.delete_project(project_id)
        messagebox.showinfo("Успех", "Проект удалён!")
        self.refresh_projects()