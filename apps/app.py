import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
from docx import Document
import os

# Variable global para almacenar la ruta de la plantilla seleccionada
plantilla_path = ""

# Historial de contratos generados
historial_contratos = []

# Función para seleccionar la plantilla de contrato
def seleccionar_plantilla():
    global plantilla_path
    plantilla_path = filedialog.askopenfilename(filetypes=[("Documentos Word", "*.docx")])
    if plantilla_path:
        lbl_plantilla.config(text=f"Plantilla seleccionada:\n{plantilla_path}")

# Función para generar el contrato
def generar_contrato():
    if not plantilla_path:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una plantilla primero.")
        return
    
    datos = {
        "nombre": entry_nombre.get(),
        "rfc": entry_rfc.get(),
        "direccion": entry_direccion.get(),
        "nombre_cliente": entry_cliente.get(),
        "rfc_cliente": entry_rfc_cliente.get(),
        "direccion_cliente": entry_direccion_cliente.get()
    }

    if not all(datos.values()):
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
        return

    # Cargar la plantilla y reemplazar los datos
    doc = Document(plantilla_path)
    for p in doc.paragraphs:
        p.text = p.text.replace("[NOMBRE]", datos["nombre"])
        p.text = p.text.replace("[RFC]", datos["rfc"])
        p.text = p.text.replace("[DIRECCION]", datos["direccion"])
        p.text = p.text.replace("[NOMBRE_CLIENTE]", datos["nombre_cliente"])
        p.text = p.text.replace("[RFC_CLIENTE]", datos["rfc_cliente"])
        p.text = p.text.replace("[DIRECCION_CLIENTE]", datos["direccion_cliente"])

    # Nombre del contrato generado
    nombre_archivo = f"Contrato_{datos['nombre']}.docx"
    doc.save(nombre_archivo)

    # Agregar al historial
    historial_contratos.append(nombre_archivo)
    actualizar_historial()

    messagebox.showinfo("Éxito", f"Contrato generado: {nombre_archivo}")

# Función para actualizar la lista de historial
def actualizar_historial():
    listbox_historial.delete(0, tk.END)  # Borra la lista actual
    for contrato in historial_contratos:
        listbox_historial.insert(tk.END, contrato)

# Función para abrir un contrato desde el historial
def abrir_contrato():
    seleccion = listbox_historial.curselection()
    if seleccion:
        contrato_seleccionado = historial_contratos[seleccion[0]]
        os.system(f'start {contrato_seleccionado}')  # En Windows
        # os.system(f'open {contrato_seleccionado}')  # En Mac
        # os.system(f'xdg-open {contrato_seleccionado}')  # En Linux

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Contratos")
root.geometry("500x500")

# Botón para seleccionar plantilla
btn_plantilla = tk.Button(root, text="Seleccionar Plantilla", command=seleccionar_plantilla)
btn_plantilla.pack(pady=5)

# Etiqueta para mostrar la plantilla seleccionada
lbl_plantilla = tk.Label(root, text="No se ha seleccionado ninguna plantilla", wraplength=400)
lbl_plantilla.pack()

# Campos de entrada para los datos del contrato
tk.Label(root, text="Nombre:").pack()
entry_nombre = tk.Entry(root)
entry_nombre.pack()

tk.Label(root, text="RFC:").pack()
entry_rfc = tk.Entry(root)
entry_rfc.pack()

tk.Label(root, text="Dirección:").pack()
entry_direccion = tk.Entry(root)
entry_direccion.pack()

tk.Label(root, text="Nombre del Cliente:").pack()
entry_cliente = tk.Entry(root)
entry_cliente.pack()

tk.Label(root, text="RFC del Cliente:").pack()
entry_rfc_cliente = tk.Entry(root)
entry_rfc_cliente.pack()

tk.Label(root, text="Dirección del Cliente:").pack()
entry_direccion_cliente = tk.Entry(root)
entry_direccion_cliente.pack()

tk.Label(root, text="Se hace o no se hace").pack()
entry_direccion_cliente = tk.Entry(root)
entry_direccion_cliente.pack()

# Botón para generar el contrato
btn_generar = tk.Button(root, text="Generar Contrato", command=generar_contrato)
btn_generar.pack(pady=10)

# Historial de contratos generados
tk.Label(root, text="Historial de Contratos:").pack()
listbox_historial = Listbox(root, height=5)
listbox_historial.pack()

# Botón para abrir un contrato desde el historial
btn_abrir = tk.Button(root, text="Abrir Contrato", command=abrir_contrato)
btn_abrir.pack(pady=5)

# Ejecutar la aplicación
root.mainloop()
