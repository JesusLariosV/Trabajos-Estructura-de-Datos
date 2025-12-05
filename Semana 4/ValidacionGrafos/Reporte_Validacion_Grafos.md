# Reporte: Validación de Propiedades de Grafos

## Algoritmo de Havel-Hakimi

### Traza Manual: Secuencia [5, 4, 3, 2, 2, 2]

**Iteración 1:**
- Secuencia inicial (ordenada): `[5, 4, 3, 2, 2, 2]`
- Eliminar d₁ = 5
- Restar 1 de los siguientes 5 elementos: `[4-1, 3-1, 2-1, 2-1, 2-1]` = `[3, 2, 1, 1, 1]`
- Reordenar: `[3, 2, 1, 1, 1]`

**Iteración 2:**
- Secuencia: `[3, 2, 1, 1, 1]`
- Eliminar d₁ = 3
- Restar 1 de los siguientes 3 elementos: `[2-1, 1-1, 1-1]` = `[1, 0, 0]`
- Resto sin modificar: `[1]`
- Resultado: `[1, 0, 0, 1]`
- Reordenar: `[1, 1, 0, 0]`

**Iteración 3:**
- Secuencia: `[1, 1, 0, 0]`
- Eliminar d₁ = 1
- Restar 1 del siguiente 1 elemento: `[1-1]` = `[0]`
- Resto: `[0, 0]`
- Resultado: `[0, 0, 0]`
- Reordenar: `[0, 0, 0]`

**Iteración 4:**
- Secuencia: `[0, 0, 0]`
- d₁ = 0 → **Todos ceros, es gráfica** ✓

**Conclusión:** La secuencia `[5, 4, 3, 2, 2, 2]` **SÍ es gráfica**.

---

## Análisis de Complejidad

### Complejidad Temporal: O(n² log n)

**Desglose:**
1. **Bucle principal:** Se ejecuta hasta n iteraciones (en el peor caso, eliminamos un elemento por iteración).
2. **Operaciones por iteración:**
   - Eliminar primer elemento: O(1) amortizado
   - Decrementar d₁ elementos: O(d₁) ≤ O(n)
   - **Reordenar la secuencia:** O(n log n) usando algoritmos de ordenamiento eficientes

**Cálculo total:**
- n iteraciones × O(n log n) por reordenamiento = **O(n² log n)**

**Nota:** Existe una optimización usando heaps (colas de prioridad) que reduce la complejidad a O(n log n), pero la implementación con ordenamiento simple es más clara didácticamente.

---

## Resultados de Casos de Prueba

### Implementación C#
- **Casos pasados:** 9/10
- **Caso fallido:** Caso 9 `[6, 1, 1, 1, 1, 1, 1]`
  - Esperado: No Gráfica
  - Obtenido: Gráfica
  - **Análisis:** Según Havel-Hakimi, esta secuencia converge a ceros y debería ser gráfica. Posible error en el caso de prueba del documento.

### Implementación Python
- **Resultado:** Idéntico a C# (9/10 casos pasados, mismo caso fallido)

### Validación del Mapa Urbano (Semana 3)
- **Secuencia extraída:** `[2, 2, 2, 2, 2, 2, 1, 1]`
- **Suma de grados:** 14 (par) ✓
- **Es gráfica:** Sí ✓
- **Es consistente:** Sí ✓

El mapa urbano de la Semana 3 es un grafo válido y consistente.

---

## Observaciones sobre el Caso 9

### Traza de `[6, 1, 1, 1, 1, 1, 1]`:

**Iteración 1:**
- Secuencia: `[6, 1, 1, 1, 1, 1, 1]` (n=7)
- Verificación inicial: max=6 < n=7 ✓, suma=12 (par) ✓
- Eliminar d₁ = 6
- Restar 1 de los siguientes 6 elementos: `[1-1, 1-1, 1-1, 1-1, 1-1, 1-1]` = `[0, 0, 0, 0, 0, 0]`
- Todos ceros → **Es gráfica**

**Conclusión:** Según el algoritmo de Havel-Hakimi, esta secuencia **SÍ es gráfica**. Representa un grafo estrella (star graph) donde un nodo central se conecta a 6 nodos periféricos, cada uno con grado 1.

**Posible explicación de la discrepancia:** El documento puede tener un error en este caso de prueba, o puede estar considerando restricciones adicionales no especificadas en el enunciado estándar de Havel-Hakimi.

---

## Conclusiones

1. **Implementación exitosa:** Ambas versiones (C# y Python) implementan correctamente el algoritmo de Havel-Hakimi.
2. **Consistencia entre lenguajes:** Los resultados son idénticos en ambas implementaciones.
3. **Validación del proyecto:** El mapa urbano de la Semana 3 cumple con todas las propiedades de un grafo simple no dirigido válido.
4. **Caso especial identificado:** El Caso 9 requiere revisión, ya que el algoritmo lo clasifica como gráfico cuando el documento espera que no lo sea.
