
# =============+ Import +==============
import tkinter
import tkinter.messagebox
from typing import Tuple
from tkinter import ttk, END
import customtkinter
import pymongo
import db as db

# =============+ Style for all +==============

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
class insertStockWin(customtkinter.CTkToplevel):
    def __init__(self, parent) -> None:
        super().__init__(parent)


        self.on_closing = None
        self.title("Inserer un nouvel élement")
        self.geometry("550x250")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.isOpen = False

        self.label = customtkinter.CTkLabel(self, text="Test")
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_closing(self):
        self._window_exists = False
        self.destroy()

class buttonStock(customtkinter.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=20, fg_color='#272727', hover_color='#414141', font=("Inter", 12), width=100, height=100,  **kwargs)

class BtnFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        

        self.button1 = buttonStock(self, text="Ajouter un\nélement", command=self.insertFrameView)
        self.button1.grid(row=0, column=0, padx=10, pady=10)

        self.button2 = buttonStock(self, text="Retirer du\nstock à un\nélement", command=self.insertFrameView)
        self.button2.grid(row=1, column=0, padx=10, pady=10)

        self.button3 = buttonStock(self, text="Retirer un\nélement", command=self.insertFrameView)
        self.button3.grid(row=2, column=0, padx=10, pady=10)

        self.button4 = buttonStock(self, text="Supprimer \ntous les\nélements", command=self.insertFrameView)
        self.button4.grid(row=3, column=0, padx=10, pady=10)

        self.button5 = buttonStock(self, text="Ajouter du\nstock à un\nélementt", command=self.insertFrameView)
        self.button5.grid(row=0, column=1, padx=10, pady=10)

        self.button6 = buttonStock(self, text="Retirer du\nstock à un\nélement", command=self.insertFrameView)
        self.button6.grid(row=1, column=1, padx=10, pady=10)
        

    def insertFrameView(self):
        self.newWin = insertStockWin(self)
        self.newWin.grab_set()


# =============+ View Table of Stock +==============
class StockViewFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.connectDb = db.Database()
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
        style.map('Treeview', background=[('selected', '#2c2c2c')])
        style.configure("Treeview.Heading",
                        background="#373737",
                        foreground="white",
                        relief="flat",
                        font=('Inter', 10))
        style.map("Treeview.Heading",
                  background=[('active', '#2c2c2c')])
        
        # =============+ Into +==============
        # =============+ Table column +==============
        columns = ('id', 'name', 'type', 'qty', 'infos')
        self.table = ttk.Treeview(master=self, columns=columns, height=20, selectmode='browse', show='headings')
        self.table.column("#1", anchor='c', minwidth=50, width=50)
        self.table.column('#2', anchor='w', minwidth=120, width=120)
        self.table.column('#3', anchor='c', minwidth=80, width=80)
        self.table.column('#4', anchor='c', minwidth=50, width=50)
        self.table.column('#4', anchor='c', minwidth=80, width=80)
        # =============+ Table head +==============
        self.table.heading('id', text='ID')
        self.table.heading('name', text="Libéllé")
        self.table.heading('type', text='Type')
        self.table.heading('qty', text="Quantité")
        self.table.heading('infos', text="Informations")
        self.table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.refreshStock()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def refreshStock(self):
        self.values = self.connectDb.getAll()
        i = 0
        for doc in self.values:
            i += 1
            self.table.insert(parent='', index='end', iid=doc["_id"], text='', values=(i, doc["name"], doc["type"], doc["qty"], doc["infos"]))

class StockApp(customtkinter.CTk):
    
    def __init__(self) -> None:
        super().__init__()


        self.on_closing = None
        self.title("StockApp")
        self.geometry("930x580")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameLeft = StockViewFrame(master=self, corner_radius=15, height=540, width=600)
        self.frameLeft.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        self.frameLeft = BtnFrame(master=self, corner_radius=15, height=540, width=260)
        self.frameLeft.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

        self.mainloop()
    
        


if __name__ == "__main__":
    app = StockApp()