# interfaz.py
# Este archivo define cómo se ve y se organiza la ventana de la aplicación.

import customtkinter as ctk

class FrameCoordenadas(ctk.CTkFrame):
    def __init__(self, master, titulo, variables, ayuda_texto):
        super().__init__(master, corner_radius=15)
        
        self.variables = variables
        
        # --- Título del Frame ---
        self.label_titulo = ctk.CTkLabel(self, text=titulo, font=ctk.CTkFont(size=20, weight="bold"))
        self.label_titulo.pack(pady=10, padx=20, anchor="w")

        # --- Frame de Entradas ---
        self.frame_entradas = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_entradas.pack(pady=10, padx=20, fill="x")

        # Entrada para la función f(x,y,z)
        self.label_funcion = ctk.CTkLabel(self.frame_entradas, text="Función f(x, y, z):", font=ctk.CTkFont(size=14))
        self.label_funcion.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.entry_funcion = ctk.CTkEntry(self.frame_entradas, placeholder_text="Ej: x**2 + y*z", width=250)
        self.entry_funcion.grid(row=0, column=1, columnspan=3, padx=5, pady=10, sticky="ew")

        # Entradas para los límites de integración
        self.entries_limites = {}
        for i, var in enumerate(variables):
            label_var = ctk.CTkLabel(self.frame_entradas, text=f"Límites de {var}:", font=ctk.CTkFont(size=14))
            label_var.grid(row=i+1, column=0, padx=5, pady=10, sticky="w")
            
            entry_inf = ctk.CTkEntry(self.frame_entradas, width=120)
            entry_inf.grid(row=i+1, column=1, padx=5, pady=10)
            
            label_hasta = ctk.CTkLabel(self.frame_entradas, text="hasta")
            label_hasta.grid(row=i+1, column=2, padx=5)

            entry_sup = ctk.CTkEntry(self.frame_entradas, width=120)
            entry_sup.grid(row=i+1, column=3, padx=5, pady=10)
            
            self.entries_limites[var] = (entry_inf, entry_sup)
        
        # --- Botón de Calcular ---
        self.boton_calcular = ctk.CTkButton(self, text="Calcular Integral", command=self.calcular)
        self.boton_calcular.pack(pady=20, padx=20)
        
        # --- Área de Resultado ---
        self.label_resultado_titulo = ctk.CTkLabel(self, text="Resultado:", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_resultado_titulo.pack(padx=20, anchor="w")
        
        self.label_resultado = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=22, family="Courier"), fg_color="#333", corner_radius=8, width=400, height=50)
        self.label_resultado.pack(pady=10, padx=20, fill="x")
        
        # --- Ayuda ---
        self.label_ayuda = ctk.CTkLabel(self, text=ayuda_texto, justify="left", wraplength=450)
        self.label_ayuda.pack(pady=10, padx=20, anchor="w")

    def calcular(self):
        # Esta función será sobreescrita por la clase principal para conectar con el backend
        pass

    def obtener_datos(self):
        funcion = self.entry_funcion.get()
        limites = {var: (inf.get(), sup.get()) for var, (inf, sup) in self.entries_limites.items()}
        return funcion, limites