# Reporte: Recorrido de Grafos (BFS y DFS)

## 1. Búsqueda en Amplitud (BFS)

### Traza Manual desde Nodo A

Grafo: A-B, A-C, B-D, B-E, C-F, E-G

**Iteración por iteración:**

| Iteración | Cola | Nodo Actual | Visitados | Nivel |
|-----------|------|-------------|-----------|-------|
| 0 (inicio) | [A] | - | {A} | 0 |
| 1 | [B, C] | A | {A, B, C} | 1 |
| 2 | [C, D, E] | B | {A, B, C, D, E} | 2 |
| 3 | [D, E, F] | C | {A, B, C, D, E, F} | 2 |
| 4 | [E, F] | D | {A, B, C, D, E, F} | - |
| 5 | [F, G] | E | {A, B, C, D, E, F, G} | 3 |
| 6 | [G] | F | {A, B, C, D, E, F, G} | - |
| 7 | [] | G | {A, B, C, D, E, F, G} | FIN |

**Resultado:** Orden BFS: `A → B → C → D → E → F → G`

**Distancias desde A:**
- A: 0, B: 1, C: 1, D: 2, E: 2, F: 2, G: 3

**Camino más corto de A a G:** `A → B → E → G` (3 aristas)

---

## 2. Búsqueda en Profundidad (DFS)

### Traza Manual Recursiva desde Nodo A

| Paso | Llamada Recursiva | Nodo Actual | Visitados Acumulados |
|------|-------------------|-------------|----------------------|
| 1 | DFS(A) | A | {A} |
| 2 | DFS(B) ← desde A | B | {A, B} |
| 3 | DFS(D) ← desde B | D | {A, B, D} |
| 4 | Retorno a B, probar E | E | {A, B, D, E} |
| 5 | DFS(G) ← desde E | G | {A, B, D, E, G} |
| 6 | Retorno a A, probar C | C | {A, B, D, E, G, C} |
| 7 | DFS(F) ← desde C | F | {A, B, D, E, G, C, F} |

**Resultado:** Orden DFS: `A → B → D → E → G → C → F`

**Observación:** DFS explora en profundidad la rama A→B→D→E→G antes de retroceder para explorar C→F.

---

## 3. Comparación BFS vs DFS

| Criterio | BFS | DFS |
|----------|-----|-----|
| **Estructura de Datos** | Cola (Queue) - FIFO | Pila (Stack) - LIFO o Recursión |
| **Orden de Exploración** | Por niveles (horizontal) | En profundidad (vertical) |
| **Complejidad Temporal** | O(V + E) | O(V + E) |
| **Complejidad Espacial** | O(V) - cola | O(h) donde h=profundidad |
| **Camino Más Corto** | ✅ SÍ (grafos no ponderados) | ❌ NO |
| **Detección de Ciclos** | Posible, menos natural | ✅ Excelente |
| **Orden de Visita (A-G)** | A→B→C→D→E→F→G | A→B→D→E→G→C→F |
| **Uso de Memoria (este grafo)** | 3 nodos máximo en cola | 4 niveles de recursión |

### Análisis de Memoria en el Grafo de Ejemplo

**BFS:**
- Nivel 0: [A] → 1 nodo
- Nivel 1: [B, C] → 2 nodos
- Nivel 2: [D, E, F] → **3 nodos (máximo)**
- Nivel 3: [G] → 1 nodo

**DFS:**
- Camino más profundo: A → B → E → G
- Profundidad máxima: **4 llamadas recursivas**

**Conclusión:** En este grafo específico, DFS usa más memoria (4 vs 3).

---

## 4. Detección de Ciclos en Grafos Dirigidos

### Algoritmo DFS Modificado

Usa 3 estados por nodo:
- `NOT_VISITED`: No explorado
- `IN_PROCESS`: En la pila de recursión actual
- `COMPLETED`: Exploración finalizada

**Lógica:**
- Si durante DFS encontramos un nodo `IN_PROCESS`, hay un ciclo (arista de retroceso).

### Ejemplo: Grafo con Ciclo

Grafo: 1→2→3→1, 3→4

**Traza:**

| Paso | Nodo | Estado | Acción | Observación |
|------|------|--------|--------|-------------|
| 1 | 1 | NOT_VISITED → IN_PROCESS | Iniciar DFS | - |
| 2 | 2 | NOT_VISITED → IN_PROCESS | Explorar desde 1 | - |
| 3 | 3 | NOT_VISITED → IN_PROCESS | Explorar desde 2 | - |
| 4 | 1 | **IN_PROCESS** (encontrado) | Intentar explorar desde 3 | **🔴 CICLO: 1→2→3→1** |

**Resultado:** Ciclo detectado correctamente.

### Ejemplo: Grafo Acíclico

Grafo: 1→2→3→4

**Resultado:** No se detecta ciclo (todos los nodos pasan a `COMPLETED` sin encontrar nodos `IN_PROCESS`).

---

## 5. Aplicaciones Prácticas

### BFS - Camino Más Corto
- **Problema:** Encontrar la ruta más corta de A a G en el grafo.
- **Solución:** BFS garantiza el camino con menor número de aristas.
- **Resultado:** A → B → E → G (3 aristas)

### DFS - Detección de Ciclos
- **Problema:** Verificar dependencias circulares en módulos de software.
- **Solución:** DFS con estados detecta ciclos en O(V + E).
- **Aplicación:** Build systems, package managers, análisis de dependencias.

---

## 6. Resultados de Ejecución

### C# Output
```
Orden BFS: A -> B -> C -> D -> E -> F -> G
Orden DFS Recursivo: A -> B -> D -> E -> G -> C -> F
Orden DFS Iterativo: A -> B -> D -> E -> G -> C -> F
Camino más corto A→G: A -> B -> E -> G (3 aristas)
Ciclo en grafo dirigido: SI
Grafo acíclico: NO tiene ciclo
```

### Python Output
Resultados idénticos a C#, confirmando la correctitud de ambas implementaciones.

---

## 7. Conclusiones

1. **BFS** es ideal para encontrar caminos más cortos en grafos no ponderados y exploración por niveles.
2. **DFS** es más eficiente para detección de ciclos, ordenamiento topológico y problemas de backtracking.
3. Ambos algoritmos tienen complejidad O(V + E), pero difieren en uso de memoria según la estructura del grafo.
4. La implementación iterativa de DFS es más segura para grafos muy profundos (evita stack overflow).
5. Las versiones C# y Python producen resultados idénticos, validando la correctitud de las implementaciones.
