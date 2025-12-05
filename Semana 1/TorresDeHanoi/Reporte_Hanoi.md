# Reporte: Torres de Hanoi (Recursividad vs Iteración)

## 1. Resolución Manual (n=3)
Para mover 3 discos de la Torre A a la Torre C:

1. **Hanoi(2, A, B)**: Mover 2 discos de A a B.
   - A -> C
   - A -> B
   - C -> B
2. **A -> C**: Mover el disco más grande de A a C.
3. **Hanoi(2, B, C)**: Mover 2 discos de B a C.
   - B -> A
   - B -> C
   - A -> C

**Total de movimientos:** 7
**Secuencia:** A->C, A->B, C->B, A->C, B->A, B->C, A->C

## 2. Comparación Recursiva vs Iterativa

| Aspecto | Recursivo | Iterativo |
| :--- | :--- | :--- |
| **Legibilidad** | Alta. El código refleja directamente la definición del problema. | Baja. Requiere entender patrones matemáticos complejos (ciclos pares/impares). |
| **Líneas de Código** | Pocas (~15 líneas). | Muchas (~50 líneas). |
| **Complejidad Espacial** | O(n) debido a la pila de llamadas. | O(n) debido al diccionario/mapa de posiciones. |
| **Complejidad Temporal** | O(2^n). | O(2^n). |
| **Rendimiento (Benchmark)** | Más rápido en C# (menos overhead de asignación de objetos). | Más lento debido a la gestión manual de estado y diccionarios. |

## 3. Resultados del Benchmark
Se ejecutó una prueba de rendimiento comparando ambas implementaciones en C#. Los resultados (en Ticks promedio) son:

| n | Recursivo (Ticks) | Iterativo (Ticks) | Factor de Diferencia |
| :--- | :--- | :--- | :--- |
| 5 | ~95 | ~293 | ~3x más lento |
| 10 | ~2,121 | ~12,959 | ~6x más lento |
| 15 | ~140,878 | ~580,256 | ~4x más lento |
| 20 | ~2,303,491 | ~5,802,465 | ~2.5x más lento |

**Conclusión:**
Aunque ambas versiones tienen la misma complejidad asintótica O(2^n), la versión recursiva es más eficiente en la práctica en este entorno debido a la simplicidad de las operaciones de pila del sistema comparado con la sobrecarga de manipular estructuras de datos (Diccionarios, HashSets) en cada paso de la versión iterativa. Además, la versión recursiva es mucho más fácil de implementar y mantener.
