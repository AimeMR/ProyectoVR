# Python - Guía de Referencia

## Tipos de Variables
- **Dinámico** (tipado dinámico, no se declara el tipo)
- **Básicos**: int, float, str, bool, None
- **Colecciones**: list, tuple, dict, set
- **Tipado opcional** con anotaciones (Python 3.5+): `variable: tipo`

## Definición de Variables
```python
numero = 10
letra = 'A'
precio = 19.99
nombre = "Juan"
# Constantes (por convención)
MAX = 100
# Con anotaciones de tipo (opcional)
edad: int = 25
```

## Variables "Intocables" y Privadas
```python
# Variables con doble guion bajo (name mangling)
class Ejemplo:
    def __init__(self):
        self.__privada = "No accesible directamente"  # Name mangling
        
# Acceso a variable con name mangling
obj = Ejemplo()
# print(obj.__privada)  # Error
print(obj._Ejemplo__privada)  # Funciona

# Variables "protegidas" (convención)
class Base:
    def __init__(self):
        self._protegida = "Accesible pero no recomendado"

# Variables especiales
__name__  # Nombre del módulo
__file__  # Ruta del archivo
__doc__   # Docstring del módulo

# Constantes predefinidas
None
True
False
NotImplemented
Ellipsis  # También representado como ...

# Funciones y métodos especiales (dunder methods)
__init__
__str__
__repr__
__add__
```

## Punteros
```python
# Python no tiene punteros explícitos
# Todas las variables son referencias a objetos

# Referencias a objetos
a = [1, 2, 3]
b = a        # b y a apuntan al mismo objeto
b.append(4)  # Modifica tanto a como b

# Para crear una copia independiente
import copy
c = copy.copy(a)      # Copia superficial
d = copy.deepcopy(a)  # Copia profunda

# Funciones como objetos de primera clase
def saludar(nombre):
    print(f"Hola {nombre}")

func = saludar  # func es una referencia a la función saludar
func("Juan")    # Imprime: Hola Juan
```

## Clases y Herencia
```python
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre
        
    def hacer_sonido(self):
        print("Sonido genérico")

class Perro(Animal):
    def __init__(self, nombre):
        super().__init__(nombre)
        
    def hacer_sonido(self):
        print("Guau!")
```

## Formato de Funciones
```python
# Función simple
def sumar(a, b):
    return a + b

# Con parámetros predeterminados
def saludar(nombre="Mundo"):
    print(f"Hola {nombre}")

# No hay sobrecarga nativa, pero se puede simular
def multiplicar(a, b):
    return a * b

# Con anotaciones de tipo
def maximo(a: int, b: int) -> int:
    return a if a > b else b

# Argumentos variables
def sumar_varios(*args):
    return sum(args)

# Argumentos con nombre
def crear_persona(**kwargs):
    return kwargs
```