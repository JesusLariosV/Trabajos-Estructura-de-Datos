# Reporte: Puente a Programación Dinámica (Escaleras)

## 1. Modificación del Problema
El problema original permitía subir 1 o 2 escalones. El reto consiste en permitir subir 1, 2 o 3 escalones a la vez.

### Nueva Recurrencia
Para llegar al escalón `n`, podemos haber llegado desde:
- El escalón `n-1` (dando un salto de 1).
- El escalón `n-2` (dando un salto de 2).
- El escalón `n-3` (dando un salto de 3).

Por lo tanto, la relación de recurrencia es:
`f(n) = f(n-1) + f(n-2) + f(n-3)`

### Nuevos Casos Base
Para que la recurrencia funcione correctamente, necesitamos definir los casos base:
- `f(0) = 1`: Hay 1 forma de estar en el suelo (no hacer nada).
- `f(n) = 0` para `n < 0`: No se puede subir escalones negativos.

Alternativamente, si definimos explícitamente los primeros valores:
- `f(1) = 1` (1)
- `f(2) = 2` (1+1, 2)
- `f(3) = 4` (1+1+1, 1+2, 2+1, 3)

## 2. Implementación

### Memoización (Top-Down)
Se utiliza un diccionario o arreglo para almacenar los resultados de `f(n)` a medida que se calculan recursivamente.
```csharp
if (memo.ContainsKey(n)) return memo[n];
long res = EscalerasMemo(n - 1) + EscalerasMemo(n - 2) + EscalerasMemo(n - 3);
memo[n] = res;
return res;
```

### Tabulación (Bottom-Up)
Se construye un arreglo `dp` de tamaño `n+1` y se llena iterativamente.
```csharp
dp[0] = 1;
for (int i = 1; i <= n; i++) {
    if (i >= 1) dp[i] += dp[i - 1];
    if (i >= 2) dp[i] += dp[i - 2];
    if (i >= 3) dp[i] += dp[i - 3];
}
```

## 3. Resultados
Para `n=10`, el número de formas es **274**.
La secuencia de Tribonacci (similar a Fibonacci pero sumando 3 términos anteriores) aparece:
1, 2, 4, 7, 13, 24, 44, 81, 149, 274...
