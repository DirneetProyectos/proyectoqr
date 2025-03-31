import qrcode
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, ttk
from PIL import Image, ImageTk

def generate_qr():
    text = entry.get()
    if not text:
        messagebox.showwarning("Advertencia", "Ingrese un texto para generar el código QR")
        return
    
    global qr_image, logo_path
    qr_type = qr_type_var.get()
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    if qr_type == "Texto":
        qr.add_data(text)
    elif qr_type == "URL":
        qr.add_data(f"http://{text}" if not text.startswith("http") else text)
    elif qr_type == "Número de Teléfono":
        qr.add_data(f"tel:{text}")
    elif qr_type == "Correo Electrónico":
        qr.add_data(f"mailto:{text}")
    elif qr_type == "Redes Sociales":
        qr.add_data(f"https://www.{text}")
    elif qr_type == "Multimedia":
        qr.add_data(f"file:///{text}")
    
    qr.make(fit=True)
    
    fill_color = color_fg.get()
    back_color = color_bg.get()
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img = img.convert("RGBA")
    
    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((50, 50))
            img.paste(logo, ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2), logo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el logo: {e}")
    
    qr_image = img
    
    img_resized = img.resize((250, 250))
    img_tk = ImageTk.PhotoImage(img_resized)
    label_qr.config(image=img_tk, bg=color_bg.get())
    label_qr.image = img_tk

def save_qr():
    if qr_image is None:
        messagebox.showwarning("Advertencia", "No hay un código QR para guardar")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
    if file_path:
        qr_image.save(file_path)
        messagebox.showinfo("Éxito", "Código QR guardado correctamente")

def choose_logo():
    global logo_path
    logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if logo_path:
        messagebox.showinfo("Logo seleccionado", "Logo cargado correctamente")

def choose_fg_color():
    color = colorchooser.askcolor()[1]
    if color:
        color_fg.set(color)

def choose_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        color_bg.set(color)
        label_qr.config(bg=color)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Generador de Código QR")
root.geometry("600x750")
root.configure(bg="#f8f9fa")

frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="raised", bd=3)
frame.pack(pady=20)

label_title = tk.Label(frame, text="Generador de Código QR", font=("Arial", 18, "bold"), bg="#ffffff", fg="#343a40")
label_title.pack(pady=10)

qr_type_var = tk.StringVar(value="Texto")
types = ["Texto", "URL", "Número de Teléfono", "Correo Electrónico", "Redes Sociales", "Multimedia"]
type_menu = ttk.Combobox(frame, textvariable=qr_type_var, values=types, state="readonly", font=("Arial", 12))
type_menu.pack(pady=5)

type_label = tk.Label(frame, text="Ingrese el contenido:", font=("Arial", 14), bg="#ffffff")
type_label.pack()

entry = tk.Entry(frame, width=50, font=("Arial", 12), relief="solid", bd=2)
entry.pack(pady=10)

button_frame = tk.Frame(frame, bg="#ffffff")
button_frame.pack(pady=10)

btn_generate = tk.Button(button_frame, text="Generar QR", command=generate_qr, bg="#007BFF", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, relief="raised")
btn_generate.grid(row=0, column=0, padx=5)

btn_logo = tk.Button(button_frame, text="Agregar Logo", command=choose_logo, bg="#28A745", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, relief="raised")
btn_logo.grid(row=0, column=1, padx=5)

btn_fg_color = tk.Button(button_frame, text="Color Código QR", command=choose_fg_color, bg="#FFC107", fg="black", font=("Arial", 12, "bold"), padx=10, pady=5, relief="raised")
btn_fg_color.grid(row=1, column=0, padx=5, pady=5)

btn_bg_color = tk.Button(button_frame, text="Color de Fondo", command=choose_bg_color, bg="#DC3545", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, relief="raised")
btn_bg_color.grid(row=1, column=1, padx=5, pady=5)

label_qr = tk.Label(frame, bg="white", relief="solid", bd=2)
label_qr.pack(pady=15)

btn_save = tk.Button(frame, text="Guardar QR", command=save_qr, bg="#17A2B8", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, relief="raised")
btn_save.pack(pady=10)

qr_image = None
logo_path = None
color_fg = tk.StringVar(value="black")
color_bg = tk.StringVar(value="white")

root.mainloop()
