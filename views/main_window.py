# Главное окно приложения согласно README.md

import tkinter as tk
from tkinter import ttk
from views.book_view import BookView
from views.reader_view import ReaderView
from views.loan_view import LoanView

class MainWindow(tk.Tk):
    def __init__(self, book_controller, reader_controller, loan_controller) -> None:
        super().__init__()
        self.title("Library Management System")
        self.geometry("900x600")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

