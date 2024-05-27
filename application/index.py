
# =============+ Import +==============
import tkinter
import tkinter.messagebox
from typing import Tuple
from tkinter import ttk, END
import customtkinter
from CTkSpinbox import *
import pymongo
import db as db

# =============+ Style for all +==============

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
class popupWin(customtkinter.CTkToplevel):
    def __init__(self, parent, title, geometry="550x250") -> None:
        super().__init__(parent)

        self.on_closing = None
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.isOpen = False
        
    def on_closing(self):
        self._window_exists = False
        self.destroy()

class modifyStockWin(popupWin):
    def __init__(self, curItem, parent, title="Modifier un nombre de stock", geometry="550x250") -> None:
        super().__init__(parent, title, geometry)
        self.labelLastStockNameT = customtkinter.CTkLabel(self, text="Nom de l'élément", anchor="center", justify="left")
        self.labelLastStockNameT.grid(row=0, column=0, sticky="nsew")
        self.labelLastStockName = customtkinter.CTkLabel(self, text=curItem['values'][1], anchor="center", text_color="green", justify="left", corner_radius=8)
        self.labelLastStockName.grid(row=1, column=0, sticky="nsew")
        self.labelLastStockNbrT = customtkinter.CTkLabel(self, text="Nombre de stock de l'élément", anchor="center", justify="left")
        self.labelLastStockNbrT.grid(row=2, column=0, sticky="nsew")
        self.labelLastStockNbr = customtkinter.CTkLabel(self, text=curItem['values'][3], anchor="center", text_color="green", justify="left", corner_radius=8)
        self.labelLastStockNbr.grid(row=3, column=0, sticky="nsew")
        self.labelReqNbrT = customtkinter.CTkLabel(self, text="Nouveau nombre de stock de l'élément", anchor="center", justify="left")
        self.labelReqNbrT.grid(row=4, column=0, sticky="nsew")
        self.inputNbr = CTkSpinbox(self, start_value=curItem['values'][3], min_value=0)
        self.inputNbr.grid(row=5, column=0, sticky="nsew", padx=50)
        self.btnAddElem = customtkinter.CTkButton(self, text="Valider", fg_color="#373737", hover_color="#414141", command=print)
        self.btnAddElem.grid(row=6, column=0 ,sticky="nsew", padx=50, pady=15)
        self.grid_columnconfigure(0, weight=1)

class insertStockWin(popupWin):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "Inserer un élement", geometry='500x350', **kwargs)
        self.infos = {}
        self.parent = parent

        # Nom de l'élement widget
        self.strName = customtkinter.StringVar()
        self.labelName = customtkinter.CTkLabel(self, text="Nom de l'élement", anchor="w", justify="left")
        self.labelName.grid(row=0, column=0, sticky="w", padx=30, pady=(20, 0), ipadx=10)
        self.inputName = customtkinter.CTkEntry(self, placeholder_text="Nom")
        self.inputName.grid(row=1, column=0, sticky="w", padx=28, ipadx=10)

        #Type de l'élement widget
        self.labelType = customtkinter.CTkLabel(self, text="Type de l'élement", anchor="w", justify="left")
        self.labelType.grid(row=0, column=1, sticky="w", padx=(30, 0), pady=(20, 0), ipadx=10)
        self.inputType = customtkinter.CTkComboBox(self, values=["Nourriture", "Boisson"])
        self.inputType.grid(row=1, column=1, sticky="w", padx=28, ipadx=10)

        #Stock déja présent de l'élement widget
        self.labelStock = customtkinter.CTkLabel(self, text="Stock de l'élement", anchor="w", justify="left")
        self.labelStock.grid(row=3, column=0, sticky="w", padx=30, pady=(20, 0), ipadx=10)
        self.inputStock = customtkinter.CTkEntry(self, placeholder_text="number")
        self.inputStock.grid(row=4, column=0, sticky="w", padx=28, ipadx=10)
        
        #Information de l'élement
        self.strInfoKey = customtkinter.StringVar()
        self.labelInfos = customtkinter.CTkLabel(self, text="Information(s) du produit", anchor='w', justify='left')
        self.labelInfos.grid(row=3, column=1, sticky="w", padx=30, pady=(20, 0), ipadx=10)
        self.inputInfoKey = customtkinter.CTkEntry(self, placeholder_text="Clé de l'info", textvariable=self.strInfoKey)
        self.inputInfoKey.grid(row=4, column=1, sticky='w', padx=28, ipadx=10)
        self.strInfoGet = customtkinter.StringVar()
        self.inputInfoGet = customtkinter.CTkEntry(self, placeholder_text="Info", textvariable=self.strInfoGet)
        self.inputInfoGet.grid(row=5, column=1, sticky='w', padx=28, pady=(5, 0), ipadx=10)

        #Ajouter une info
        self.btnAdd = customtkinter.CTkButton(self, width=50, height=20, text='Ajouter', fg_color="#373737", hover_color='#414141', command=lambda: self.addInfo(self.inputInfoKey.get(), self.inputInfoGet.get())) #command=lambda: self.addInfo(self.strInfoKey.get(), self.strInfoGet.get()) )
        self.btnAdd.grid(row=5, column=1, sticky='e', padx=(0, 15), pady=(5, 0))

        #Listing des infos ajoutées
        columns = ('key', 'info')
        self.table = ttk.Treeview(master=self, columns=columns, height=5, selectmode='browse', show='headings')
        self.table.column("#1", anchor='c', width=25, minwidth=25)
        self.table.column('#2', anchor='w', minwidth=25)
        # =============+ Table head +==============
        self.table.heading('key', text='Clé')
        self.table.heading('info', text="Info")
        self.table.grid(row=6, column=1, sticky='nsew', padx=20, pady=10)
        
        self.btnAddElem = customtkinter.CTkButton(self, text="Valider", fg_color="#373737", hover_color="#414141", command=self.addToStock)
        self.btnAddElem.grid(row=6, column=0 ,sticky="nsew", padx=20, pady=20)
        
    def addInfo(self, key, info):
        if not key or not info:
            print("Erreur")
            return
        try: 
            if self.infos[key]:
                print("same")
        except:
            self.infos[key] = info
            self.table.insert(parent='', index='end', text='', values=(key, info))
            self.inputInfoGet.delete(0, END)
            self.inputInfoKey.delete(0, END)
            
    def addToStock(self):
        name = self.inputName.get()
        type = self.inputType.get()
        try:
            nbrStock = int(self.inputStock.get())
        except:
            nbrStock = False
            
        self.infos = self.infos
        
        if len(name) > 1 and nbrStock:
            print(name, type, nbrStock, self.infos)
            self.principal = self.parent.master.frameLeft
            self.principal.connectDb.insertStock(name, type, nbrStock, self.infos)
            self.principal.refreshStock()
            self.destroy()
        else:
            print("Il manque des infos")




class buttonStock(customtkinter.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=20, fg_color='#272727', hover_color='#414141', font=("Inter", 12), width=100, height=100,  **kwargs)

class BtnFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.frameLeft = self.master.frameLeft

        # Add element (Already fix)
        self.button1 = buttonStock(self, text="Ajouter un\nélement", command=self.insertFrameView)
        self.button1.grid(row=0, column=0, padx=10, pady=10)

        self.button2 = buttonStock(self, text="Modifier du\nstock à un\nélement", command=self.modifyStockFrameView)
        self.button2.grid(row=1, column=0, padx=10, pady=10)

        # Delete element (Already fix)
        self.button3 = buttonStock(self, text="Retirer un\nélement", command=self.deleteFrameView)
        self.button3.grid(row=2, column=0, padx=10, pady=10)

        # Delete all elements (on fixing)
        self.button4 = buttonStock(self, text="Supprimer \ntous les\nélements", command=self.deleteAllFrameView)
        self.button4.grid(row=3, column=0, padx=10, pady=10)
        

        self.button6 = buttonStock(self, text="Modifier un\nélement", command=self.insertFrameView)
        self.button6.grid(row=0, column=1, padx=10, pady=10)
        

    def insertFrameView(self):
        self.newWin = insertStockWin(self)
        self.newWin.grab_set()
        
    def deleteFrameView(self):
        self.frameLeft.connectDb.deleteStock(self.frameLeft.curItemID)
        self.frameLeft.refreshStock()

    def deleteAllFrameView(self):
        self.frameLeft.connectDb.deleteAllStock()
        self.frameLeft.refreshStock()

    def modifyStockFrameView(self):
        self.newWin = modifyStockWin(self.frameLeft.curItem, self)

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
        self.table.bind('<ButtonRelease-1>', self.selectedItem)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def refreshStock(self):
        for i in self.table.get_children():
            self.table.delete(i)
        self.values = self.connectDb.getAll()
        i = 0
        for doc in self.values:
            print(doc)
            i += 1
            self.table.insert(parent='', index='end', iid=doc["_id"], text='', values=(i, doc["name"], doc["type"], doc["qty"], doc["infos"]))
    
    def selectedItem(self, a):
        self.curItemID = self.table.focus()
        self.curItem = self.table.item(self.curItemID)
        
        
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
        self.frameRight = BtnFrame(master=self, corner_radius=15, height=540, width=260)
        self.frameRight.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

        self.mainloop()
    
        


if __name__ == "__main__":
    app = StockApp()