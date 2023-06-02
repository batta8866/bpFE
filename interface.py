import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def run_program():
    output_text.delete(1.0, tk.END)
    try:
        process = subprocess.Popen(["python", "P.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output_text.insert(tk.END, output)
        process.communicate()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Poli App Perras ♔")
root.geometry("950x450")
root.configure(bg="#ffe6e6")  # cambiar el color de fondo a rosa claro

output_frame = tk.Frame(root, borderwidth=2, relief="groove", bg="#ffe6e6")  # cambiar el color del marco a rosa claro
output_frame.pack(padx=10, pady=10, fill="both", expand=True)

output_text = tk.Text(output_frame, height=20, width=70, bg="#fff5f5", fg="#ff69b4", font=("Helvetica", 12))
output_text.pack(padx=5, pady=5, fill="both", expand=True)

run_button = tk.Button(root, text="ʕ•́ᴥ•̀ʔっ", command=run_program, bg="#ff69b4", fg="white",
                       font=("Helvetica", 10, "bold"), padx=10, pady=5)
run_button.pack(pady=10)

root.mainloop()