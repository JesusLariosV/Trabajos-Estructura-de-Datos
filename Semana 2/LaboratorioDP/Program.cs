using System;
using System.Collections.Generic;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("--- Laboratorio de Consolidación DP ---\n");

        // Ejercicio 2
        Console.WriteLine("Ejercicio 2: Formas de formar un número (1, 2)");
        int n = 10;
        Console.WriteLine($"Formas({n}) Ingenuo: {FormasIngenuo(n)}");
        Console.WriteLine($"Formas({n}) Memo:    {FormasMemo(n, new Dictionary<int, long>())}");
        Console.WriteLine($"Formas({n}) Tabla:   {FormasTabla(n)}");
        Console.WriteLine();

        // Ejercicio 3
        Console.WriteLine("Ejercicio 3: Cambio de Monedas [1, 3, 4]");
        int amount = 6;
        Console.WriteLine($"Min Monedas para {amount}: {MinMonedas(amount)}");
        Console.WriteLine($"Min Monedas para 10: {MinMonedas(10)}");
        Console.WriteLine();

        // Ejercicio 4
        Console.WriteLine("Ejercicio 4: Fibonacci Corregido");
        Console.WriteLine($"Fibonacci(5): {FibonacciCorregido(5)}");
        Console.WriteLine($"Fibonacci(10): {FibonacciCorregido(10)}");
        Console.WriteLine();

        // Mini-Proyecto
        Console.WriteLine("Mini-Proyecto: Suma Máxima Sin Adyacentes");
        int[] arr = { 3, 2, 7, 10 };
        Console.WriteLine($"Arr: [{string.Join(", ", arr)}]");
        Console.WriteLine($"Max Suma: {MaxSumaSinAdyacentes(arr)}");
        
        int[] arr2 = { 3, 2, 5, 10, 7 };
        Console.WriteLine($"Arr: [{string.Join(", ", arr2)}]");
        Console.WriteLine($"Max Suma: {MaxSumaSinAdyacentes(arr2)}");
    }

    // --- Ejercicio 2 ---
    static long FormasIngenuo(int n)
    {
        if (n <= 0) return 1; // Base case correction: usually f(0)=1 (do nothing), f(negative)=0. But prompt says n<=0 return 1 for simplicity or specific logic? Let's stick to standard:
        // Wait, prompt says: if n <= 0: return 1. Let's follow prompt.
        if (n == 1) return 1;
        return FormasIngenuo(n - 1) + FormasIngenuo(n - 2);
    }

    static long FormasMemo(int n, Dictionary<int, long> memo)
    {
        if (n <= 0) return 1;
        if (n == 1) return 1;
        if (memo.ContainsKey(n)) return memo[n];
        
        long res = FormasMemo(n - 1, memo) + FormasMemo(n - 2, memo);
        memo[n] = res;
        return res;
    }

    static long FormasTabla(int n)
    {
        if (n <= 0) return 1;
        if (n == 1) return 1;
        
        long[] dp = new long[n + 1];
        dp[0] = 1;
        dp[1] = 1;
        
        for (int i = 2; i <= n; i++)
        {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n];
    }

    // --- Ejercicio 3 ---
    static int MinMonedas(int n)
    {
        int[] monedas = { 1, 3, 4 };
        if (n == 0) return 0;
        if (n < 0) return int.MaxValue;

        int[] dp = new int[n + 1];
        Array.Fill(dp, int.MaxValue);
        dp[0] = 0;

        for (int i = 1; i <= n; i++)
        {
            foreach (var moneda in monedas)
            {
                if (i >= moneda && dp[i - moneda] != int.MaxValue)
                {
                    dp[i] = Math.Min(dp[i], 1 + dp[i - moneda]);
                }
            }
        }
        return dp[n] == int.MaxValue ? -1 : dp[n];
    }

    // --- Ejercicio 4 ---
    static int FibonacciCorregido(int n)
    {
        if (n <= 0) return 0; // Handle 0
        if (n == 1) return 1;
        
        // Error 1: Size was n, needs n+1 to access index n
        int[] dp = new int[n + 1]; 
        dp[1] = 1;
        
        // Error 2: Range was range(2, n) which excludes n. Needs to go up to n (inclusive)
        for (int i = 2; i <= n; i++) 
        {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        // Error 3: Accessing dp[n] is now safe
        return dp[n]; 
    }

    // --- Mini-Proyecto: House Robber ---
    static int MaxSumaSinAdyacentes(int[] nums)
    {
        if (nums == null || nums.Length == 0) return 0;
        if (nums.Length == 1) return nums[0];
        
        int[] dp = new int[nums.Length];
        dp[0] = nums[0];
        dp[1] = Math.Max(nums[0], nums[1]);
        
        for (int i = 2; i < nums.Length; i++)
        {
            // Option 1: Rob current house (i) + max of i-2
            // Option 2: Skip current house, take max of i-1
            dp[i] = Math.Max(nums[i] + dp[i - 2], dp[i - 1]);
        }
        
        return dp[nums.Length - 1];
    }
}
