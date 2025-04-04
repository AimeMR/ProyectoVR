# Java - Guía de Referencia

## Tipos de Variables
- **Primitivos**: int, float, double, char, boolean, byte, short, long
- **Referencia**: String, Object, clases personalizadas
- **Wrapper**: Integer, Float, Double, Character, Boolean (versiones objeto de primitivos)

## Definición de Variables
```java
int numero = 10;
char letra = 'A';
float precio = 19.99f;
String nombre = "Juan";
// Constantes
final int MAX = 100;
// A partir de Java 10
var valor = 5.6;
```

## Punteros
```java
// Java no tiene punteros explícitos
// Todas las variables de objetos son referencias

// Referencia a objeto
String str = new String("Hola");

// Referencia a arrays
int[] array = new int[5];

// Referencia a método (Java 8+)
Function<Integer, Integer> funcion = x -> x * x;
BiFunction<Integer, Integer, Integer> sumar = (a, b) -> a + b;
```

## Clases y Herencia
```java
class Animal {
    protected String nombre;
    
    public Animal(String n) {
        nombre = n;
    }
    
    public void hacerSonido() {
        System.out.println("Sonido genérico");
    }
}

class Perro extends Animal {
    public Perro(String n) {
        super(n);
    }
    
    @Override
    public void hacerSonido() {
        System.out.println("Guau!");
    }
}
```

## Formato de Funciones
```java
// Función simple
public int sumar(int a, int b) {
    return a + b;
}

// No hay parámetros predeterminados nativos
public void saludar() {
    saludar("Mundo");
}
public void saludar(String nombre) {
    System.out.println("Hola " + nombre);
}

// Sobrecarga de métodos
public float multiplicar(float a, float b) {
    return a * b;
}
public int multiplicar(int a, int b) {
    return a * b;
}

// Método genérico
public <T extends Comparable<T>> T maximo(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}
```