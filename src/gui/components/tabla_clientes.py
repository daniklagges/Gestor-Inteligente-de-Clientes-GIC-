import tkinter as tk
from tkinter import ttk


class TablaClientes(tk.Frame):

    COLUMNAS = [
        ("nombre", "Nombre", 150),
        ("email", "Email", 180),
        ("telefono", "Telefono", 130),
        ("tipo_cliente", "Tipo", 90),
        ("activo", "Estado", 70),
        ("direccion", "Direccion", 200),
    ]

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._datos = []
        self._crear_widgets()

    def _crear_widgets(self):
        cols = [c[0] for c in self.COLUMNAS]
        scroll_y = tk.Scrollbar(self, orient="vertical")
        scroll_x = tk.Scrollbar(self, orient="horizontal")
        self.tree = ttk.Treeview(self, columns=cols, show="headings",
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, selectmode="browse")
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        for col_id, texto, ancho in self.COLUMNAS:
            self.tree.heading(col_id, text=texto)
            self.tree.column(col_id, width=ancho, minwidth=50)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        self.tree.tag_configure("inactivo", foreground="gray")
        self.tree.tag_configure("premium", foreground="#8B5CF6")
        self.tree.tag_configure("corporativo", foreground="#0369A1")

    def cargar_clientes(self, clientes):
        self.tree.delete(*self.tree.get_children())
        self._datos = []
        for cliente in clientes:
            datos = cliente.to_dict()
            self._datos.append(datos)
            estado = "Activo" if datos["activo"] else "Inactivo"
            valores = (datos["nombre"], datos["email"], datos["telefono"],
                datos["tipo_cliente"], estado, datos["direccion"])
            tags = []
            if not datos["activo"]:
                tags.append("inactivo")
            elif datos["tipo_cliente"] == "Premium":
                tags.append("premium")
            elif datos["tipo_cliente"] == "Corporativo":
                tags.append("corporativo")
            self.tree.insert("", "end", values=valores, tags=tags)

    def obtener_seleccion(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return None
        index = self.tree.index(seleccion[0])
        if index < len(self._datos):
            return self._datos[index]
        return None
