import tkinter as tk
import subprocess



def run_program():
    output_text.delete(1.0, tk.END)
    result = subprocess.run(["python", "P.py"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    output_text.insert(tk.END, result.stdout.decode())
root = tk.Tk()
root.title("Poli App Perras ♔")
root.geometry("950x450")
root.configure(bg="#ffe6e6")  # cambiar el color de fondo a rosa claro
output_frame = tk.Frame(root, borderwidth=2, relief="groove", bg="#ffe6e6")  # cambiar el color del marco a rosa claro
output_frame.pack(padx=10, pady=10, fill="both", expand=True)
output_text = tk.Text(output_frame, height=20, width=70, bg="#fff5f5", fg="#ff69b4", font=("Helvetica", 12))  # cambiar el color de fondo y el color del texto a rosa claro y rosa oscuro, respectivamente, y cambiar la fuente a Helvetica de tamaño 12
output_text.pack(padx=5, pady=5, fill="both", expand=True)
run_button = tk.Button(root, text="ʕ•́ᴥ•̀ʔっ", command=run_program, bg="#ff69b4", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)  # cambiar el color de fondo y el color del texto del botón a rosa oscuro y blanco, respectivamente, y cambiar la fuente a Helvetica de tamaño 14 y negrita, y agregar un relleno horizontal y vertical
run_button.pack(pady=10)
root.mainloop()