import tkinter
import tkinter.messagebox
from typing import Tuple
from tkinter import ttk, END
import customtkinter
import sqlite3
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class StockViewFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # =============+ Style for Treeview +==============
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1e1e1e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#272727",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",
                        background="#373737",
                        foreground="white",
                        relief="flat",
                        font=('Inter', 10))
        style.map("Treeview.Heading",
                  background=[('active', '#2c2c2c')])
        
        # =============+ Into +==============
        columns = ('id', 'name', 'type', 'qty', 'infos')
        self.table = ttk.Treeview(master=self, columns=columns, height=17, selectmode='browse', show='headings')
        self.table.column("#1", anchor='c', minwidth=50, width=50)
        self.table.column('#2', anchor='w', minwidth=120, width=120)
        self.table.column('#3', anchor='c', minwidth=80, width=80)
        self.table.column('#4', anchor='c', minwidth=50, width=50)
        self.table.column('#4', anchor='c', minwidth=80, width=80)

        self.table.heading('id', text='ID')
        self.table.heading('name', text="Libéllé")
        self.table.heading('type', text='Type')
        self.table.heading('qty', text="Quantité")
        self.table.heading('infos', text="Informations")
        self.table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

class StockApp(customtkinter.CTk):
    
    def __init__(self) -> None:
        super().__init__()


        self.on_closing = None
        self.title("StockApp")
        self.geometry("1100x580")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.frameLeft = StockViewFrame(master=self, corner_radius=15, height=400, width=600)
        self.frameLeft.grid(row=0, column=0, padx=20, pady=20)
        


if __name__ == "__main__":
    app = StockApp()
    app.mainloop()