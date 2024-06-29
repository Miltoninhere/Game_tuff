import tkinter as tk
import json
from datetime import datetime, timedelta

num_muertes = 0
tiempo_juego = timedelta(seconds=0)
inicio_juego = datetime.now()

def incrementar_muertes():
    global num_muertes
    num_muertes += 1
    label_muertes.config(text=f"Muertes: {num_muertes}")
    guardar_datos()

def guardar_datos():
    data = {
        "num_muertes": num_muertes,
        "tiempo_juego_segundos": tiempo_juego.total_seconds()
    }
    with open("datos_juego.json", "w", encoding="utf-8") as f:
        json.dump(data, f)

def actualizar_tiempo():
    global tiempo_juego, inicio_juego
    ahora = datetime.now()
    tiempo_transcurrido = ahora - inicio_juego
    tiempo_juego = timedelta(seconds=tiempo_transcurrido.total_seconds())
    tiempo_str = str(tiempo_juego).split('.')[0]
    label_tiempo.config(text=f"Tiempo en Juego:\n{tiempo_str}")
    root.after(1000, actualizar_tiempo)

def cargar_datos():
    global num_muertes, tiempo_juego, inicio_juego
    try:
        with open("datos_juego.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            num_muertes = data.get("num_muertes", 0)
            tiempo_juego = timedelta(seconds=data.get("tiempo_juego_segundos", 0))
            inicio_juego = datetime.now() - tiempo_juego
    except FileNotFoundError:
        pass

root = tk.Tk()
root.title("")
root.geometry("200x110")
root.resizable(False, False)

cargar_datos()

label_tiempo = tk.Label(root, text=f"Tiempo en Juego:\n{tiempo_juego}", font=("Arial", 10))
label_tiempo.pack(pady=10)

label_muertes = tk.Label(root, text=f"Muertes: {num_muertes}", font=("Arial", 10))
label_muertes.pack()

frame_botones = tk.Frame(root)
frame_botones.pack()

btn_incrementar = tk.Button(frame_botones, text="+", command=incrementar_muertes, font=("Arial", 10))
btn_incrementar.pack(side=tk.LEFT, padx=5)

def on_cerrar():
    guardar_datos()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_cerrar)
actualizar_tiempo()
root.mainloop()
