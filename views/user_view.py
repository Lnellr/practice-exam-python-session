import tkinter as tk
from tkinter import ttk, messagebox

class UserView(ttk.Frame):
    def __init__(self, parent, user_controller) -> None:
        super().__init__(parent)
        self.user_controller = user_controller
        self.create_widgets()
        self.refresh_users()

    def create_widgets(self) -> None:
        # --- Форма добавления пользователя ---
        form = ttk.LabelFrame(self, text="Добавить пользователя")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Имя:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.e_username = ttk.Entry(form)
        self.e_username.grid(row=0, column=1, sticky="ew", padx=5, pady=4)

        ttk.Label(form, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.e_email = ttk.Entry(form)
        self.e_email.grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        ttk.Label(form, text="Роль:").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.cb_role = ttk.Combobox(form, values=("admin", "manager", "developer"), state="readonly")
        self.cb_role.set("developer")
        self.cb_role.grid(row=2, column=1, sticky="ew", padx=5, pady=4)

        ttk.Button(form, text="Добавить", command=self.add_user).grid(row=3, column=0, columnspan=2, pady=8)
        form.columnconfigure(1, weight=1)

        # --- Таблица пользователей ---
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "username", "email", "role", "registration_date"),
            show="headings"
        )
        for col, title, width in [
            ("id", "ID", 60),
            ("username", "Имя", 160),
            ("email", "Email", 220),
            ("role", "Роль", 120),
            ("registration_date", "Регистрация", 160),
        ]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width)

        self.tree.pack(fill="both", expand=True, side="left")

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        # --- Панель действий ---
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=10, pady=6)
        ttk.Button(bar, text="Обновить список", command=self.refresh_users).pack(side="left", padx=5)
        ttk.Button(bar, text="Удалить выбранного", command=self.delete_selected).pack(side="left", padx=5)

    def refresh_users(self) -> None:
        # очистка
        for i in self.tree.get_children():
            self.tree.delete(i)

        users = self.user_controller.get_all_users()
        for u in users:
            # поддержка и моделей-объектов, и dict
            get = (lambda obj, name: getattr(obj, name) if hasattr(obj, name) else obj.get(name))
            uid = get(u, "id")
            username = get(u, "username")
            email = get(u, "email")
            role = get(u, "role")
            reg = get(u, "registration_date")
            if hasattr(reg, "isoformat"):
                reg = reg.isoformat()
            self.tree.insert("", "end", values=(uid, username, email, role, reg))

    def add_user(self) -> None:
        username = self.e_username.get().strip()
        email = self.e_email.get().strip()
        role = self.cb_role.get().strip()

        if not username:
            messagebox.showerror("Ошибка", "Имя не может быть пустым.")
            return
        if not email:
            messagebox.showerror("Ошибка", "Email не может быть пустым.")
            return
        if not role:
            messagebox.showerror("Ошибка", "Выберите роль.")
            return

        try:
            self.user_controller.add_user(username, email, role)
            messagebox.showinfo("Успех", "Пользователь добавлен.")
            self.refresh_users()
            self.e_username.delete(0, tk.END)
            self.e_email.delete(0, tk.END)
            self.cb_role.set("developer")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_selected(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Внимание", "Выберите пользователя для удаления.")
            return
        user_id = self.tree.item(sel[0])["values"][0]
        try:
            self.user_controller.delete_user(user_id)
            messagebox.showinfo("Успех", "Пользователь удалён.")
            self.refresh_users()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))