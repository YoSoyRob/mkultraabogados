import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import subprocess

def buscar_archivos(directorio, nombre_archivo):
    resultados = []
    for raiz, _, archivos in os.walk(directorio):
        for archivo in archivos:
            if nombre_archivo.lower() in archivo.lower():
                resultados.append(os.path.join(raiz, archivo))
    
    return resultados

def buscar_carpetas(directorio, nombre_carpeta):
    resultados = []
    for raiz, carpetas, _ in os.walk(directorio):
        for carpeta in carpetas:
            if nombre_carpeta.lower() in carpeta.lower():
                resultados.append(os.path.join(raiz, carpeta))
    
    return resultados

def seleccionar_directorio():
    root = tk.Tk()
    root.withdraw()
    directorio = filedialog.askdirectory(title="Selecciona un directorio")
    return directorio

def abrir_archivo(ruta):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(ruta)
        elif os.name == 'posix':  # macOS o Linux
            subprocess.call(['xdg-open', ruta])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

def solicitar_entrada(mensaje):
    root = tk.Tk()
    root.withdraw()
    return simpledialog.askstring("Entrada", mensaje)

def main():
    directorio = seleccionar_directorio()
    if not directorio:
        messagebox.showinfo("Información", "No se seleccionó ningún directorio. Saliendo...")
        return
    
    while True:
        comando = solicitar_entrada("Ingrese el comando (buscar archivo / buscar carpeta / salir):")
        if not comando:
            continue
        comando = comando.strip().lower()
        
        if comando == "buscar archivo":
            nombre_archivo = solicitar_entrada("Ingresa el nombre del archivo a buscar:")
            if not nombre_archivo:
                continue
            resultados = buscar_archivos(directorio, nombre_archivo)
            if resultados:
                resultado_texto = "\n".join([f"[{idx}] {resultado}" for idx, resultado in enumerate(resultados)])
                opcion = simpledialog.askstring("Resultados", f"Archivos encontrados:\n{resultado_texto}\n\nIngrese el número del archivo a abrir o 'n' para salir:")
                if opcion and opcion.lower() != 'n':
                    try:
                        indice = int(opcion)
                        if 0 <= indice < len(resultados):
                            abrir_archivo(resultados[indice])
                        else:
                            messagebox.showwarning("Advertencia", "Índice fuera de rango.")
                    except ValueError:
                        messagebox.showwarning("Advertencia", "Entrada inválida.")
            else:
                messagebox.showinfo("Información", "No se encontraron archivos con ese nombre.")
        
        elif comando == "buscar carpeta":
            nombre_carpeta = solicitar_entrada("Ingresa el nombre de la carpeta a buscar:")
            if not nombre_carpeta:
                continue
            resultados = buscar_carpetas(directorio, nombre_carpeta)
            if resultados:
                resultado_texto = "\n".join(resultados)
                messagebox.showinfo("Carpetas encontradas", resultado_texto)
            else:
                messagebox.showinfo("Información", "No se encontraron carpetas con ese nombre.")
        
        elif comando == "salir":
            messagebox.showinfo("Información", "Saliendo de la aplicación.")
            break
        else:
            messagebox.showwarning("Advertencia", "Comando no reconocido. Usa 'buscar archivo', 'buscar carpeta' o 'salir'.")

if __name__ == "__main__":
    main()