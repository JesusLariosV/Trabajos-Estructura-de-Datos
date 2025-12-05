# Reporte: Proyecto de Teoría de Grafos (Mapa de Tráfico)

## 1. Diseño del Modelo
Se ha modelado un mapa de tráfico de una pequeña ciudad con 8 intersecciones (Vértices A-H) y 12 conexiones principales.

### Representación Elegida: Lista de Adyacencia
Se eligió utilizar **Listas de Adyacencia** (`Dictionary<T, List<(T, double)>>`) por las siguientes razones:
1.  **Eficiencia en Memoria:** El grafo es **disperso**. Con 8 vértices, una matriz de adyacencia ocuparía 64 celdas, muchas de ellas vacías. La lista solo almacena las conexiones reales (19 aristas en el modelo dirigido completo).
2.  **Iteración de Vecinos:** Para algoritmos de navegación (como Dijkstra o BFS que veremos luego), es más eficiente iterar solo sobre los vecinos existentes que recorrer una fila entera de ceros en una matriz.
3.  **Flexibilidad:** Permite añadir vértices y aristas dinámicamente sin redimensionar una matriz fija.

## 2. Implementación Técnica
### C# (Constructor del Grafo)
- Se creó una clase genérica `Graph<T>`.
- Soporta grafos dirigidos y no dirigidos.
- Incluye métodos para exportar la estructura a archivos de texto plano, facilitando la interoperabilidad.
- **Manejo de No Dirigidos:** Se implementó añadiendo la arista en ambas direcciones (`A->B` y `B->A`). Al exportar, se deduplicaron las aristas para evitar redundancia en el archivo.

### Python (Analista de Datos)
- Se desarrolló un script para cargar los archivos generados por C#.
- Calcula métricas clave:
    - **Grados de Entrada/Salida:** Fundamental para entender el flujo de tráfico.
    - **Densidad:** Mide qué tan conectado está el grafo.

## 3. Análisis de Resultados

### Grafo No Dirigido (Calles de Doble Sentido)
Representa la infraestructura base donde todas las calles permiten ir y volver.
- **Densidad:** 0.250 (Baja, típico de redes viales).
- **Conectividad:** Todos los nodos tienen grado 2, excepto G y H (grado 1), que actúan como terminales periféricos.

### Grafo Dirigido (Mapa Completo con Sentidos)
Incluye las restricciones de tráfico (calles de un solo sentido).
- **Vértice A (Centro):**
    - *Out-degree:* 3 (Puede ir a G, B, C).
    - *In-degree:* 3 (Recibe de B, C, H).
    - Es un punto neurálgico bien conectado.
- **Vértice H (Estadio):**
    - Recibe tráfico del Norte (B) y Hospital (G).
    - Envía tráfico de vuelta al Centro (A) y Hospital (G).
    - Muestra cómo los grafos dirigidos modelan flujos asimétricos (ej. ir al estadio es rápido desde el norte, pero volver requiere ir al centro).

## 4. Reflexión: Matriz vs Lista
Si hubiéramos usado una **Matriz de Adyacencia**:
- **Ventaja:** Verificar si existe una calle directa entre dos puntos sería O(1) instantáneo.
- **Desventaja:** Para encontrar "a dónde puedo ir desde A", tendríamos que revisar las 8 posibles columnas, lo cual es ineficiente si A solo conecta con 3 lugares.
- **Conclusión:** Dado que `m << n^2` (19 aristas es mucho menor que 64 posibles), la Lista de Adyacencia es la decisión técnica correcta.
