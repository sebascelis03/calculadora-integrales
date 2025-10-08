# main.py
# Archivo principal para ejecutar la aplicación.

import customtkinter as ctk
from interfaz import FrameCoordenadas
from calculo import resolver_integral_triple

# --- Apariencia de la Aplicación ---
ctk.set_appearance_mode("dark")  # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuración de la Ventana Principal ---
        self.title("Calculadora de Integrales Triples")
        self.geometry("550x620")
        self.resizable(False, False)

        # --- Título Principal ---
        self.label_titulo_app = ctk.CTkLabel(self, text="Calculadora de Integrales Triples", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_titulo_app.pack(pady=(20, 10))

        # --- Selector de Coordenadas ---
        self.selector_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.selector_frame.pack(pady=10)
        self.selector = ctk.CTkSegmentedButton(
            self.selector_frame, 
            values=["Rectangulares", "Cilíndricas", "Esféricas"],
            command=self.cambiar_frame
        )
        self.selector.set("Rectangulares")
        self.selector.pack()

        # --- Contenedor para los Frames ---
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=10)
        self.frames = {}
        
        # --- Crear los frames para cada sistema de coordenadas ---
        for F, nombre, variables, ayuda in [
            (FrameCoordenadas, 'rectangulares', ['z', 'y', 'x'], "Orden de integración: dzdydx.\nLas funciones de límite para z pueden usar x, y.\nLas funciones de límite para y pueden usar x."),
            (FrameCoordenadas, 'cilindricas', ['z', 'r', 'theta'], "Orden: dzdrd(theta). f(x,y,z) se convierte a f(r*cos(theta), r*sin(theta), z).\nEl Jacobiano 'r' se añade automáticamente."),
            (FrameCoordenadas, 'esfericas', ['rho', 'phi', 'theta'], "Orden: d(rho)d(phi)d(theta).\nEl Jacobiano 'rho^2 * sin(phi)' se añade automáticamente.")
        ]:
            frame = F(self.container, nombre.capitalize(), variables, ayuda)
            self.frames[nombre] = frame
            # Conectar el botón de este frame a la función de cálculo
            frame.boton_calcular.configure(command=lambda f=frame: self.realizar_calculo(f))
            
        self.cambiar_frame("Rectangulares")

    def cambiar_frame(self, nombre_frame):
        # Oculta todos los frames
        for frame in self.frames.values():
            frame.pack_forget()
        
        # Muestra el frame seleccionado
        frame_seleccionado = self.frames[nombre_frame.lower()]
        frame_seleccionado.pack(fill="both", expand=True)
    
    def realizar_calculo(self, frame_activo):
        nombre_coordenadas = frame_activo.label_titulo.cget("text").lower()
        funcion, limites = frame_activo.obtener_datos()
        variables_orden = frame_activo.variables # ['z', 'y', 'x'] o similar

        if not funcion or not all(lim[0] and lim[1] for lim in limites.values()):
            frame_activo.label_resultado.configure(text="Rellene todos los campos.")
            return

        # Llamar a la función del backend
        resultado = resolver_integral_triple(
            funcion_str=funcion,
            var_str=variables_orden,
            limites=limites,
            coordenadas=nombre_coordenadas
        )

        # Mostrar el resultado en la interfaz
        if isinstance(resultado, str): # Si hubo un error
            frame_activo.label_resultado.configure(text=resultado, text_color="orange")
        else:
            frame_activo.label_resultado.configure(text=f"{resultado:.6f}", text_color="cyan")


if __name__ == "__main__":
    app = App()
    app.mainloop()