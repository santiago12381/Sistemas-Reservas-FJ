import random
import string


# ===========================
# EXCEPCIONES PERSONALIZADAS
# ===========================

class LongitudInvalidaError(Exception):
    pass


class EntradaInvalidaError(Exception):
    pass


class ContrasenaInvalidaError(Exception):
    pass


# ===========================
# CLASE CONTRASEÑA
# ===========================

class Contrasena:
    
    caracteres_especiales = "¿¡?=)(/¨*+-%&$#!"
    
    def __init__(self, longitud):
        self.longitud = longitud
        self.password = ""
        
    def generar_contrasena(self):
        
        mayusculas = string.ascii_uppercase
        minusculas = string.ascii_lowercase
        numeros = string.digits
        especiales = Contrasena.caracteres_especiales
        
        todos = mayusculas + minusculas + numeros + especiales
        
        caracteres = []
        
        # Agregar obligatorios 
        caracteres.append(random.choice(mayusculas))
        caracteres.append(random.choice(minusculas))
        caracteres.append(random.choice(numeros))
        caracteres.append(random.choice(especiales))
        
        while len(caracteres) < self.longitud:
            
            caracter = random.choice(todos)
            
            if caracter not in caracteres:
                caracteres.append(caracter)
                
        random.shuffle(caracteres)
        
        self.password = "".join(caracteres)            
        
        return self.password
    
    def validar_contrasena(self):
        
        if len(self.password) < 8:
            raise ContrasenaInvalidaError(
                "La contraseña debe tener minimo 8 caracteres"
            )
            
        if not any(c.isupper() for c in self.password):
            raise ContrasenaInvalidaError(
                "Falta una letra mayuscula"
            )    
            
        if not any(c.islower() for c in self.password):
            raise ContrasenaInvalidaError(
                "Falta una letra minuscula"
            ) 
            
        if not any(c.isdigit() for c in self.password):       
            raise ContrasenaInvalidaError(
                "Falta un numero"
            )
            
        if not any(
            c in Contrasena.caracteres_especiales
            for c in self.password
        ):
            raise ContrasenaInvalidaError(
                "Falta un caracter especial"
            )    
            
        if len(set(self.password)) != len(self.password):
            raise ContrasenaInvalidaError(
                "La contrasena tiene caracteres repetdos"
            )    
        
        return True
    

# ===========================
# CLASE COFRE
# ===========================

class Cofre:
    
    def __init__(self, nombre, puntos):
        self.nombre = nombre
        self.puntos = puntos        
        

# ============================
# HERENCIA
# ============================

class CofreComun(Cofre):
    
    def __init__(self):
        super().__init__("Comun", 10)
        
        
class CofreRaro(Cofre):
    
    def __init__(self):
        super().__init__("Raro", 25)                
        
        
class CofreLegendario(Cofre):
    
    def __init__(self):
        super().__init__("Legendario", 50)        
        
        
class CofreFalso(Cofre):
    
    def __init__(self):
        super().__init__("Falso", -20)
        
        
# ============================
# CLASE JUEGO
# ============================

class JuegoCazador:
    
    def __init__(self):
        self.puntos = 0
        
    def obtener_cofre(self):
        
        cofres = [
            CofreComun(),
            CofreRaro(),
            CofreLegendario()
        ]                    
        
        return random.choice(cofres)
    
    def iniciar(self):
        
        print("=" * 50)
        print("🪖🪖 JUEGO CAZADOR DE CONTRASEÑAS 🪖🪖")
        print("=" * 50)
        
        while True:
            
            try:
                
                entrada = input(
                    "\nIngre la longitud de la contraseña: "
                )
                
                if not entrada.isdigit():
                    raise EntradaInvalidaError(
                        "Debe ingresar un numero"
                    )
                    
                longitud = int(entrada)
                    
                if longitud < 8:
                   raise LongitudInvalidaError(
                       "La longitud minima es 8"
                    )
                
                contrasena = Contrasena(longitud)
                
                password = contrasena.generar_contrasena()
                
                print("\nContraseña generada:")
                print(password)
                
                contrasena.validar_contrasena()
                
                cofre = self.obtener_cofre()
                
                if cofre.nombre == "Comun":
                   print("\n🤺🤺 Has obtenido un cofre comun")
                   
                elif cofre.nombre == "Raro":   
                   print("\n🤖👽🫣 Has obtenido un cofre raro")
                   
                elif cofre.nombre == "Legendario":
                    print("\n🦾💍💎🏅 ¡Has obtenido un cofre legendario!")
                    
                print(f"🥇🏆💵 Puntos ganados: {cofre.puntos}")       
                
                self.puntos += cofre.puntos
                
            except (
                EntradaInvalidaError,
                LongitudInvalidaError,
                ContrasenaInvalidaError
            ) as error:
                
                print("\nERROR:", error)
                
                cofre = CofreFalso()
                
                print(
                    f"\n👻🤣🤣 Perdiste cofre falso jejeje 👻🤣🤣"
                )           
                
                print(
                    f"💸✈️ Puntos perdidos: "
                    f"{abs(cofre.puntos)}"
                )
                
                self.puntos += cofre.puntos
                
            except Exception as error:
                
                print("\n🐧🐧Ocurrio un error inesperado 🐧🐧")
                print(error)
                
            print(f"\n💰💰😍 Puntaje acumulado: {self.puntos}")
            
            opcion = input(
                "\n¿Quieres intentarlo una vez mas? (s/n): "
            ).lower()
            
            if opcion != "s":
                break
            
        print("\nJuego finalizado")
        print(f"Puntaje final: {self.puntos}")
        
        
# ==========================
# PROGRAMA PRINCIPAL
# ==========================

if __name__ == "__main__":
    
    juego = JuegoCazador()
    juego.iniciar() 