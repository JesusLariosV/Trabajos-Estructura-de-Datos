# Reporte: Laboratorio de Consolidación DP

## Ejercicio 1: Detección de Patrones

### Análisis de Árboles
- **Función A (Tribonacci):** `f(n) = f(n-1) + f(n-2) + f(n-3)`.
    - Tiene **muchos subproblemas repetidos**. Por ejemplo, para calcular `f(4)`, se necesita `f(3)`, `f(2)` y `f(1)`. A su vez, `f(3)` necesita `f(2)` y `f(1)`. `f(2)` se calcula múltiples veces.
    - **Veredicto:** Ideal para DP.

- **Función B (Suma Acumulativa):** `f(n) = f(n-1) + n`.
    - Estructura lineal: `f(4) -> f(3) -> f(2) -> f(1)`.
    - No hay ramificaciones, cada estado se visita una sola vez.
    - **Veredicto:** No necesita DP (es una simple recursión lineal o bucle).

- **Función C (Factorial):** `f(n) = n * f(n-1)`.
    - Estructura lineal similar a la Función B.
    - **Veredicto:** No necesita DP.

## Ejercicio 2: Transformación Guiada (Formas de formar un número)
El problema es equivalente a Fibonacci (pero con un desfase en los índices dependiendo de la definición base).
- **Ingenuo:** Recalcula exponencialmente los mismos valores.
- **Memoización:** Guarda resultados en un diccionario. Complejidad O(n).
- **Tabulación:** Llena un arreglo iterativamente. Complejidad O(n).

## Ejercicio 3: Cambio de Monedas [1, 3, 4]
Objetivo: Mínimo de monedas para formar `n`.

### Traza Manual (n=6)
| n | Cálculo | Resultado (Monedas) |
|---|---|---|
| 0 | Base | 0 |
| 1 | 1 + dp[0] | 1 (moneda 1) |
| 2 | 1 + dp[1] | 2 (1+1) |
| 3 | min(1+dp[2], 1+dp[0]) | 1 (moneda 3) |
| 4 | min(1+dp[3], 1+dp[1], 1+dp[0]) | 1 (moneda 4) |
| 5 | min(1+dp[4], 1+dp[2], 1+dp[1]) | 2 (4+1 o 1+4) |
| 6 | min(1+dp[5], 1+dp[3], 1+dp[2]) | 2 (3+3) |

Resultado para n=6: **2 monedas** (3 + 3).

## Ejercicio 4: Debugging DP
Errores encontrados y corregidos en el código de Fibonacci:
1.  **Tamaño del Array:** `dp = [0] * n` era insuficiente para acceder al índice `n`. Se corrigió a `n + 1`.
2.  **Rango del Bucle:** `range(2, n)` en Python excluye `n`. Se debe iterar hasta `n` inclusive (o `n+1` en el rango). En C# `i <= n`.
3.  **Acceso Final:** Al corregir el tamaño, el retorno `dp[n]` es seguro.

## Mini-Proyecto: Suma Máxima Sin Adyacentes
**Problema:** Encontrar la suma máxima en un arreglo sin sumar elementos adyacentes (House Robber).

**Enfoque DP:**
Para cada casa `i`, tenemos dos opciones:
1.  **Robar la casa `i`:** Sumamos su valor `nums[i]` al máximo acumulado hasta `i-2` (`dp[i-2]`).
2.  **No robar la casa `i`:** Mantenemos el máximo acumulado hasta `i-1` (`dp[i-1]`).

Recurrencia: `dp[i] = max(nums[i] + dp[i-2], dp[i-1])`.

**Resultados:**
- `[3, 2, 7, 10]` -> Max: 13 (3 + 10)
- `[3, 2, 5, 10, 7]` -> Max: 15 (3 + 5 + 7 no se puede por adyacencia 5-7? No, 5 y 7 no son adyacentes si hay 10 en medio. Indices: 0, 2, 4. 3+5+7=15. Correcto.)
