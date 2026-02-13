import tkinter as tk
from tkinter import ttk, messagebox
from src.services.cliente_service import ClienteService
from src.exceptions.validation_errors import GICValidationError
from src.exceptions.database_errors import RegistroDuplicadoError


class ClienteFormDialog:

    def __init__(self, parent, service, cliente_existente=None):
        self.service = service
        self.cliente_existente = cliente_existente
        self.resultado = None
        self.es_edicion = cliente_existente is not None
        self.top = tk.Toplevel(parent)
        self.top.title("Editar Cliente" if self.es_edicion else "Nuevo Cliente")
        self.top.geometry("480x550")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()
        self._crear_variables()
        self._crear_formulario()
        if self.es_edicion:
            self._cargar_datos()
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.top.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.top.winfo_height()) // 2
        self.top.geometry(f"+{x}+{y}")

    def _crear_variables(self):
        self.tipo_var = tk.StringVar(value="Regular")
        self.nombre_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.nivel_var = tk.StringVar(value="Gold")
        self.asesor_var = tk.StringVar()
        self.rut_var = tk.StringVar()
        self.razon_social_var = tk.StringVar()
        self.rubro_var = tk.StringVar()
        self.contacto_var = tk.StringVar()
        self.empleados_var = tk.StringVar(value="1")

    def _crear_formulario(self):
        main_frame = ttk.Frame(self.top, padding=20)
        main_frame.pack(fill="both", expand=True)
        row = 0
        ttk.Label(main_frame, text="Tipo de Cliente:").grid(row=row, column=0, sticky="w", pady=5)
        tipo_combo = ttk.Combobox(main_frame, textvariable=self.tipo_var,
            values=["Regular", "Premium", "Corporativo"],
            state="readonly" if not self.es_edicion else "disabled", width=25)
        tipo_combo.grid(row=row, column=1, sticky="ew", pady=5)
        tipo_combo.bind("<<ComboboxSelected>>", lambda _: self._actualizar_campos())
        row += 1
        ttk.Separator(main_frame, orient="horizontal").grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        campos_basicos = [("Nombre:", self.nombre_var), ("Email:", self.email_var),
            ("Telefono:", self.telefono_var), ("Direccion:", self.direccion_var)]
        for label, var in campos_basicos:
            row += 1
            ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky="w", pady=3)
            ttk.Entry(main_frame, textvariable=var, width=28).grid(row=row, column=1, sticky="ew", pady=3)
        row += 1
        self.extra_frame = ttk.LabelFrame(main_frame, text="Datos adicionales", padding=10)
        self.extra_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        self._actualizar_campos()
        row += 1
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Guardar" if not self.es_edicion else "Actualizar",
            command=self._guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.top.destroy).pack(side="left", padx=5)
        main_frame.columnconfigure(1, weight=1)

    def _actualizar_campos(self):
        for widget in self.extra_frame.winfo_children():
            widget.destroy()
        tipo = self.tipo_var.get()
        if tipo == "Premium":
            ttk.Label(self.extra_frame, text="Nivel:").grid(row=0, column=0, sticky="w", pady=3)
            ttk.Combobox(self.extra_frame, textvariable=self.nivel_var,
                values=["Gold", "Platinum", "Diamond"], state="readonly", width=25).grid(row=0, column=1, sticky="ew", pady=3)
            ttk.Label(self.extra_frame, text="Asesor:").grid(row=1, column=0, sticky="w", pady=3)
            ttk.Entry(self.extra_frame, textvariable=self.asesor_var, width=28).grid(row=1, column=1, sticky="ew", pady=3)
        elif tipo == "Corporativo":
            campos = [("RUT Empresa:", self.rut_var), ("Razon Social:", self.razon_social_var),
                ("Rubro:", self.rubro_var), ("Contacto:", self.contacto_var), ("Empleados:", self.empleados_var)]
            for i, (label, var) in enumerate(campos):
                ttk.Label(self.extra_frame, text=label).grid(row=i, column=0, sticky="w", pady=2)
                ttk.Entry(self.extra_frame, textvariable=var, width=28).grid(row=i, column=1, sticky="ew", pady=2)
        else:
            ttk.Label(self.extra_frame, text="Sin campos adicionales", foreground="gray").grid(row=0, column=0, pady=5)
        self.extra_frame.columnconfigure(1, weight=1)

    def _cargar_datos(self):
        c = self.cliente_existente
        self.tipo_var.set(c.tipo_cliente)
        self.nombre_var.set(c.nombre)
        self.email_var.set(c.email)
        self.telefono_var.set(c.telefono)
        self.direccion_var.set(c.direccion)
        if c.tipo_cliente == "Premium":
            self.nivel_var.set(c.nivel_premium)
            self.asesor_var.set(c.asesor_dedicado)
        elif c.tipo_cliente == "Corporativo":
            self.rut_var.set(c.rut_empresa)
            self.razon_social_var.set(c.razon_social)
            self.rubro_var.set(c.rubro)
            self.contacto_var.set(c.contacto_comercial)
            self.empleados_var.set(str(c.cantidad_empleados))
        self._actualizar_campos()

    def _guardar(self):
        tipo = self.tipo_var.get()
        datos = {"nombre": self.nombre_var.get(), "email": self.email_var.get(),
            "telefono": self.telefono_var.get(), "direccion": self.direccion_var.get()}
        if tipo == "Premium":
            datos["nivel_premium"] = self.nivel_var.get()
            datos["asesor_dedicado"] = self.asesor_var.get() or "Sin asignar"
        elif tipo == "Corporativo":
            datos["rut_empresa"] = self.rut_var.get()
            datos["razon_social"] = self.razon_social_var.get()
            datos["rubro"] = self.rubro_var.get() or "No especificado"
            datos["contacto_comercial"] = self.contacto_var.get()
            try:
                datos["cantidad_empleados"] = int(self.empleados_var.get())
            except ValueError:
                messagebox.showerror("Error", "Empleados debe ser un numero")
                return
        try:
            if self.es_edicion:
                self.resultado = self.service.actualizar_cliente(self.cliente_existente.id, **datos)
            else:
                self.resultado = self.service.crear_cliente(tipo, **datos)
            self.top.destroy()
        except GICValidationError as e:
            messagebox.showerror("Error de validacion", str(e))
        except RegistroDuplicadoError as e:
            messagebox.showerror("Duplicado", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
