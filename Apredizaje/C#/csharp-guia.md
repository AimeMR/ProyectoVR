# C# - Guía de Referencia

## Tipos de Variables
- **Primitivos**: int, float, double, char, bool, decimal
- **Referencia**: string, object, dynamic
- **Valor**: struct, enum
- **Nullable**: int?, double? (para tipos que aceptan null)

## Definición de Variables
```csharp
int numero = 10;
char letra = 'A';
float precio = 19.99f;
string nombre = "Juan";
// Constantes
const int MAX = 100;
// Inferencia de tipos
var valor = 5.6;
// Nullable
int? posibleNumero = null;
```

## Punteros
```csharp
// Debe estar en un bloque 'unsafe'
unsafe
{
    // Declaración de punteros
    int* ptr;
    char* charPtr;
    void* voidPtr;

    // Asignación
    int x = 10;
    int* ptr = &x;

    // Desreferenciación
    int valor = *ptr;

    // Aritmética de punteros
    int[] arr = { 1, 2, 3, 4, 5 };
    fixed (int* p = &arr[0])
    {
        int* p2 = p;
        p2++;       // p2 ahora apunta al segundo elemento
    }
}

// Delegates (alternativa segura a punteros a funciones)
delegate int OperacionDelegate(int a, int b);
OperacionDelegate operacion = Sumar;
```

## Clases y Herencia
```csharp
class Animal
{
    protected string nombre;
    
    public Animal(string n)
    {
        nombre = n;
    }
    
    public virtual void HacerSonido()
    {
        Console.WriteLine("Sonido genérico");
    }
}

class Perro : Animal
{
    public Perro(string n) : base(n) {}
    
    public override void HacerSonido()
    {
        Console.WriteLine("Guau!");
    }
}
```

## Formato de Funciones
```csharp
// Función simple
public int Sumar(int a, int b)
{
    return a + b;
}

// Con parámetros opcionales
public void Saludar(string nombre = "Mundo")
{
    Console.WriteLine($"Hola {nombre}");
}

// Sobrecarga de métodos
public float Multiplicar(float a, float b)
{
    return a * b;
}
public int Multiplicar(int a, int b)
{
    return a * b;
}

// Método genérico
public T Maximo<T>(T a, T b) where T : IComparable
{
    return a.CompareTo(b) > 0 ? a : b;
}
```