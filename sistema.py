from abc import ABC, abstractmethod
from datetime import datetime

# =================== LOG ================
def registrar_log(tipo, mensaje):
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} [{tipo}] {mensaje}\n")
        
# ================== EXCEPCIONES ===================
class ErrorSistema(Exception):
    pass

class ErrorCliente(ErrorSistema):
    pass

class ErrorServicio(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass

# ================== CLASE ABSTRACTA ================
class Entidad(ABC):
    def __init__(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ErrorSistema("Nombre invalido")
        self.nombre = nombre.strip()
        
# ================== CLIENTE ==================
class Cliente(Entidad):
    def __init__(self, nombre, identificacion):
        super().__init__(nombre)
        
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ErrorCliente("Identificacion invalida")
        
        self.__identificacion = identificacion.strip()
        
    def get_identificacion(self):
        return  self.__identificacion  
        
# ================== SERVICIO ABSTRACTO =================
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ErrorServicio("Nombre de servicio invalido")
        
        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise ErrorServicio("precio base invalido")
        
        self.nombre = nombre.strip()
        self.precio_base = precio_base
   
    @abstractmethod
    def calcular_costo(self, duracion=1, descuento=0, impuesto=True):
        pass
    
    @abstractmethod
    def descripcion(self):
        pass
    
# =================== SERVICIOS ================
class ReservaSala(Servicio):
    def calcular_costo(self, duracion=1, descuento=0, impuesto=True):
        costo = self.precio_base * duracion
        if impuesto:
            costo *= 1.1
        return costo - (costo * descuento)
    
    def descripcion(self):
        return f"Sala: {self.nombre}"
    
class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion=1, descuento=0, impuesto=True):
        costo = self.precio_base * duracion
        if impuesto:
            costo *= 1.2
        return costo - (costo * descuento)
    
    def descripcion(self):
        return f"Equipo: {self.nombre}"
    
class Asesoria(Servicio):
    def calcular_costo(self, duracion=1, descuento=0, impuesto=True):
        costo = self.precio_base * duracion
        if impuesto:
            costo *= 1.3
        return costo - (costo * descuento)
    
    def descripcion(self):
        return f"Asesoria: {self.nombre}"
   
# ===================== RESERVA =================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Cliente invalido")
        
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Servicio invalido")
        
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorReserva("Duracion invalida")
        
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        
    def confirmar(self):
        self.estado = "Confirmada"
        registrar_log("INFO", f"Reservac confirmada: {self.cliente.nombre}")
        
    def cancelar(self):
        self.estado = "Cancelada"
        registrar_log("INFO", f"Reservac cancelada: {self.cliente.nombre}") 
        
    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(
                self.duracion,
                descuento=0.1,
                impuesto=True
            )
        except Exception as e:
            registrar_log("ERROR", str(e))
            raise ErrorReserva("Error en calculo de costo") from e
        else:
            print("\n--- DETALLE RESERVA ---")
            print(f"Cliente: {self.cliente.nombre}")
            print(f"Servicio: {self.servicio.descripcion()}")
            print(f"Duracion: {self.duracion}")
            print(f"Estado: {self.estado}")
            print(f"Costo total: {costo}")
        finally:
            registrar_log("INFO", f"Reserva prosesada: {self.cliente.nombre}")
            
# ===================== SISTEMA ================
class Sistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        
    def agregar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ErrorSistema("objeto cliente invalido")
        self.clientes.append(cliente)
        
    def agregar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ErrorSistema("objeto servicio invalido")
        self.servicios.append(servicio)
        
    def crear_reserva(self, cliente, servicio, duracion):
        reserva = Reserva(cliente, servicio, duracion)  
        self.reservas.append(reserva)
        return reserva
    
    def listar_clientes(self):
        print("\nCLIENTES REGISTRADOS:")
        for c in self.clientes:
            print(f"- {c.nombre}")
            
    def listar_reservas(self):
        print("\nRESERVAS:")
        for r in self.reservas:
            print(f"- {r.cliente.nombre} | {r.servicio.descripcion()} | {r.estado}")
            
# ================== SIMULACION =====================
def simulacion():
    sistema = Sistema()
    
    try:
        c1 = Cliente("Santiago", "123")
        sistema.agregar_cliente(c1) 
        
        s1 = ReservaSala("VIP", 100)
        sistema.agregar_servicio(s1)
        
        r1 = sistema.crear_reserva(c1, s1, 2)
        r1.confirmar()
        r1.procesar()
        
    except Exception as e:
        registrar_log("ERROR", str(e))
        
    # Errores controlados
    try:
        Cliente("", "000")
    except Exception as e:
        registrar_log("ERROR", str(e))
                                      
    try:
        AlquilerEquipo("proyector", -10)
    except Exception as e:
        registrar_log("ERROR", str(e))
        
    # Mas pruebas (10+)
    for i in range(1, 9):
        try:
            c = Cliente(f"Cliente{i}", str(i))
            sistema.agregar_cliente(c)
            s = Asesoria(f"IT", 200)
            r = sistema.crear_reserva(c, s, i)
            
            if i % 2 == 0:
                r.cancelar()
            else:
                r.confirmar()
            
            r.procesar()
        
        except Exception as e:
            registrar_log("ERROR", str(e))
     
    # Error final
    try:
        sistema.crear_reserva("mal", s, 2) 
    except Exception as e:
        registrar_log("ERROR", str(e))
        
    sistema.listar_clientes()
    sistema.listar_reservas()  
    
    print("\n✅ Sistema funcionando correctamente sin detenerse.")  
    
# ================== MAIN =================
if __name__ == "__main__":
    simulacion()    