from tkinter import ttk
import tkinter as tk
from datetime import datetime
import math
import pytz
from ttkthemes import ThemedTk

class RelojApp:
    def __init__(self, root):
        self.root = root
        self.root.set_theme("radiance")  # Establece el tema "radiance" de ttkthemes
        
        self.root.title("Reloj Analógico y Digital")
        self.root.geometry("400x550")
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_app)
        
        self.root.configure(bg="#000000")  # Fondo negro
        
        self.root.tk_setPalette(background="#000000", foreground="#FFFFFF")  # Establece colores de fondo y primer plano
        
        self.canvas_analogico = tk.Canvas(root, width=400, height=400, bg="#000000")
        self.canvas_analogico.pack()
        
        self.reloj_digital = tk.Label(root, font=("Courier", 36), bg="#000000", fg="#FFFFFF")  # Texto en blanco
        self.reloj_digital.pack(pady=10)
        
        self.fecha_label = tk.Label(root, font=("Helvetica", 14), bg="#000000", fg="#FFFFFF")  # Texto en blanco
        self.fecha_label.pack(pady=10)
        
        self.estacion_label = tk.Label(root, font=("Helvetica", 14), bg="#000000", fg="#FFFFFF")  # Texto en blanco
        self.estacion_label.pack(pady=10)
        
        self.actualizar_reloj()
    
    def obtener_estacion(self, now):
        mes = now.month
        if 3 <= mes <= 5:
            return "Primavera"
        elif 6 <= mes <= 8:
            return "Verano"
        elif 9 <= mes <= 11:
            return "Otoño"
        else:
            return "Invierno"
    
    def actualizar_reloj(self):
        tz = pytz.timezone("America/Bogota")  # Zona horaria de Colombia
        now = datetime.now(tz)
        hora_actual = now.strftime("%H:%M:%S")
        fecha_actual = now.strftime("%A, %d de %B de %Y")
        estacion_actual = self.obtener_estacion(now)
        
        self.reloj_digital.config(text=hora_actual)
        self.fecha_label.config(text=fecha_actual)
        self.estacion_label.config(text=f"Estación: {estacion_actual}")
        self.dibujar_reloj_analogico(now)
        self.root.after(1000, self.actualizar_reloj)
    
    def dibujar_reloj_analogico(self, now):
        self.canvas_analogico.delete("all")
        
        centro_x = 200
        centro_y = 200
        radio = 150
        
        # Dibujar el círculo del reloj
        self.canvas_analogico.create_oval(centro_x - radio, centro_y - radio, centro_x + radio, centro_y + radio, width=2, outline="#FFFFFF")  # Borde blanco
        
        # Dibujar los marcadores para cada minuto
        for i in range(60):
            angulo_marcador = math.radians(90 - i * 6)
            x_marcador = centro_x + (radio - 10) * math.cos(angulo_marcador)
            y_marcador = centro_y - (radio - 10) * math.sin(angulo_marcador)
            self.canvas_analogico.create_oval(x_marcador - 2, y_marcador - 2, x_marcador + 2, y_marcador + 2, fill="#FFFFFF")  # Marcadores en blanco
        
        # Dibujar los números de las horas
        for i in range(12):
            angulo_numero = math.radians(90 - i * 30)
            x_numero = centro_x + (radio - 30) * math.cos(angulo_numero)
            y_numero = centro_y - (radio - 30) * math.sin(angulo_numero)
            self.canvas_analogico.create_text(x_numero, y_numero, text=str(12 if i == 0 else i), font=("Helvetica", 16), fill="#FFFFFF")  # Números en blanco
        
        # Obtener las coordenadas de las manecillas
        segundo = now.second
        minuto = now.minute
        hora = now.hour % 12  # Asegurarse de que la hora esté en un formato de 12 horas
        
        # Dibujar la manecilla de las horas
        angulo_hora = math.radians(90 - (hora * 30 + minuto * 0.5))
        x_hora = centro_x + radio * 0.4 * math.cos(angulo_hora)
        y_hora = centro_y - radio * 0.4 * math.sin(angulo_hora)
        self.canvas_analogico.create_line(centro_x, centro_y, x_hora, y_hora, width=6, fill="#FF00FF")  # Manecilla de horas en magenta
        
        # Dibujar la manecilla de los minutos
        angulo_minuto = math.radians(90 - minuto * 6)
        x_minuto = centro_x + radio * 0.6 * math.cos(angulo_minuto)
        y_minuto = centro_y - radio * 0.6 * math.sin(angulo_minuto)
        self.canvas_analogico.create_line(centro_x, centro_y, x_minuto, y_minuto, width=4, fill="#00FFFF")  # Manecilla de minutos en cian
        
        # Dibujar la manecilla de los segundos
        angulo_segundo = math.radians(90 - segundo * 6)
        x_segundo = centro_x + radio * 0.7 * math.cos(angulo_segundo)
        y_segundo = centro_y - radio * 0.7 * math.sin(angulo_segundo)
        self.canvas_analogico.create_line(centro_x, centro_y, x_segundo, y_segundo, width=2, fill="#FF0000")  # Manecilla de segundos en rojo
    
    def cerrar_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = ThemedTk(theme="radiance")  # Crea una ventana ThemedTk con el tema "radiance" de ttkthemes
    app = RelojApp(root)
    root.mainloop()
