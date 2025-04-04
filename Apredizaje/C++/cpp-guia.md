# C++ - Guía de Referencia

## Tipos de Variables
- **Primitivos**: int, float, double, char, bool
- **Compuestos**: array, struct, class, enum
- **Modificadores**: short, long, unsigned, signed

## Definición de Variables
```cpp
int numero = 10;
char letra = 'A';
float precio = 19.99;
// Constantes
const int MAX = 100;
// Auto (inferencia de tipos, C++11)
auto valor = 5.6;
```

## Punteros
```cpp
// Declaración de punteros
int* ptr;         // Puntero a entero
char* charPtr;    // Puntero a carácter
void* voidPtr;    // Puntero genérico

// Asignación
int x = 10;
int* ptr = &x;    // ptr almacena la dirección de x

// Desreferenciación
int valor = *ptr; // valor = 10

// Aritmética de punteros
int arr[5] = {1, 2, 3, 4, 5};
int* p = arr;     // p apunta al primer elemento
p++;              // p ahora apunta al segundo elemento

// Punteros a funciones
int (*funcPtr)(int, int) = sumar;
```

## Clases y Herencia
```cpp
class Animal {
protected:
    string nombre;
public:
    Animal(string n) : nombre(n) {}
    virtual void hacerSonido() {
        cout << "Sonido genérico" << endl;
    }
};

class Perro : public Animal {
public:
    Perro(string n) : Animal(n) {}
    void hacerSonido() override {
        cout << "Guau!" << endl;
    }
};
```

## Formato de Funciones
```cpp
// Función simple
int sumar(int a, int b) {
    return a + b;
}

// Con parámetros predeterminados
void saludar(string nombre = "Mundo") {
    cout << "Hola " << nombre << endl;
}

// Sobrecarga de funciones
float multiplicar(float a, float b) {
    return a * b;
}
int multiplicar(int a, int b) {
    return a * b;
}

// Función plantilla
template <typename T>
T maximo(T a, T b) {
    return (a > b) ? a : b;
}
```