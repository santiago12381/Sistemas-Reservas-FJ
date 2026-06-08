import tkinter as tk
from tkinter import messagebox


# ==========================
# Clase Usuario (LOGIN)
# ==========================
class Usuario:
    def __init__(self):
        self._usuario = "programacion"
        self._password = "programacion"
        
    def validar(self, usuario_ingresado, password_ingresada):
        return usuario_ingresado == self._usuario and password_ingresada == self._password
    
    
# ==========================
# Clase ReservaSala
# ==========================
class ReservaSala:
    def __init__(self, usuario, hora_inicio, tarifa_hora):
        self._usuario = usuario
        self._hora_inicio = None
        self._tarifa_hora = tarifa_hora
        self._hora_fin = None
        self.registrar_inicio(hora_inicio) 
        
    def registrar_inicio(self, hora):
        if hora < 0:
            return False
        self._hora_inicio = hora
        return True
    
    def registrar_fin(self, hora):
        if hora <= self._hora_inicio:
            return False
        self._hora_fin = hora
        return True
    
    def calcular_costo(self, hora_fin):
        if hora_fin <= self._hora_inicio:
            return None
        return (hora_fin - self._hora_inicio) * self._tarifa_hora
    
    def obtener_usuario(self):
        return self._usuario
    
    
# ==========================
# Aplicacion Principal
# ==========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Room Reservation System")
        
        self.reservas = []
        
        tk.Label(root, text="User Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(root, text="start Hour").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(root, text="Rate per Hour").grid(row=2, column=0, padx=5, pady=5)
        
        self.entry_user = tk.Entry(root)
        self.entry_start = tk.Entry(root)
        self.entry_rate = tk.Entry(root)
        
        self.entry_user.grid(row=0, column=1)
        self.entry_start.grid(row=1, column=1)
        self.entry_rate.grid(row=2, column=1)
        
        tk.Button(root, text="Create Reservation",
                  command=self.crear_reserva).grid(row=3, column=0, columnspan=2, pady=5)
        
        self.listbox = tk.Listbox(root, width=40)
        self.listbox.grid(row=4, column=0, columnspan=2, pady=5)
        
        tk.Label(root, text="End Hour").grid(row=5, column=0, padx=5, pady=5)
        self.entry_end = tk.Entry(root)
        self.entry_end.grid(row=5, column=1)
        
        tk.Button(root, text="Close Reservation",
                  command=self.cerrar_reserva).grid(row=6, column=0, columnspan=2, pady=5)
        
    # Crear reserva 
    def crear_reserva(self):
        usuario = self.entry_user.get().strip()
        
        if usuario == "":
            messagebox.showerror("Error", "User name cannot be empty")
            return
        
        try:
            hora_inicio = float(self.entry_start.get())
            tarifa = float(self.entry_rate.get())
        except ValueError:
            messagebox.showerror("Error", "Start hour and rate must be numeric")
            return
        
        if hora_inicio < 0 or tarifa <= 0:
            messagebox.showerror("Error", "values must be positive")
            return
           
        reserva = ReservaSala(usuario, hora_inicio, tarifa)
        self.reservas.append(reserva)
        
        self.listbox.insert(tk.END, f"{usuario} - Start: {hora_inicio}")
        
        messagebox.showinfo("Success", "Reservation created successfully")
        
        self.entry_user.delete(0, tk.END)
        self.entry_start.delete(0, tk.END)
        self.entry_rate.delete(0, tk.END)
        
    # Cerrar reserva
    def cerrar_reserva(self):
        seleccion = self.listbox.curselection()
        
        if not seleccion:
            messagebox.showerror("Error", "select a reservation")
            return
        
        try:
            hora_fin = float(self.entry_end.get())
        except ValueError:
            messagebox.showerror("Error", "End hour must be numeric")
            return
        
        reserva = self.reservas[seleccion[0]]
        
        if not reserva.registrar_fin(hora_fin):
            messagebox.showerror("Error", "End hour must be greater than start hour")
            return
        
        costo = reserva.calcular_costo(hora_fin)
        
        messagebox.showinfo("Total cost", f"Total cost: ${costo:.2f}")   
        
        self.entry_end.delete(0, tk.END)
        
        
# ==========================
# Ventana Login
# ==========================
def login():
    user = entry_user_login.get()
    password = entry_pass_login.get()
    
    usuario = Usuario()
    
    if usuario.validar(user, password):
        login_window.destroy()
        main_window = tk.Tk()
        App(main_window)
        main_window.mainloop()
    else:
        messagebox.showerror("Login Error", "Invalid credentials")
        
        
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="User").grid(row=0, column=0, padx=5, pady=5)
tk.Label(login_window, text="password").grid(row=1, column=0, padx=5, pady=5)

entry_user_login = tk.Entry(login_window)
entry_pass_login = tk.Entry(login_window, show="*")

entry_user_login.grid(row=0, column=1)
entry_pass_login.grid(row=1, column=1)

tk.Button(login_window, text="Login",
          command=login).grid(row=2, column=0, columnspan=2, pady=5)

login_window.mainloop()