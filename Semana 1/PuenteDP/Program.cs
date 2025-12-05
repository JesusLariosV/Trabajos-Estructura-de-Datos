using System;
using System.Collections.Generic;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Puente a DP: Problema de las Escaleras (1, 2, 3 pasos)");
        
        int n = 10;
        Console.WriteLine($"\nCalculando formas de subir {n} escalones:");
        
        // Memoization
        var memo = new Dictionary<int, long>();
        long resMemo = EscalerasMemo(n, memo);
        Console.WriteLine($"Memoization: {resMemo}");
        
        // Tabulation
        long resTab = EscalerasTabulacion(n);
        Console.WriteLine($"Tabulación:  {resTab}");
        
        if (resMemo == resTab)
        {
            Console.WriteLine("¡Resultados coinciden!");
        }
        else
        {
            Console.WriteLine("ERROR: Resultados difieren.");
        }

        Console.WriteLine("\nTabla de primeros valores:");
        for (int i = 1; i <= 10; i++)
        {
            Console.WriteLine($"n={i}: {EscalerasTabulacion(i)}");
        }
    }

    // Top-Down (Memoization)
    static long EscalerasMemo(int n, Dictionary<int, long> memo)
    {
        if (n < 0) return 0;
        if (n == 0) return 1;
        
        if (memo.ContainsKey(n)) return memo[n];
        
        long res = EscalerasMemo(n - 1, memo) + 
                   EscalerasMemo(n - 2, memo) + 
                   EscalerasMemo(n - 3, memo);
        
        memo[n] = res;
        return res;
    }

    // Bottom-Up (Tabulation)
    static long EscalerasTabulacion(int n)
    {
        if (n < 0) return 0;
        if (n == 0) return 1;
        
        long[] dp = new long[n + 1];
        dp[0] = 1;
        
        for (int i = 1; i <= n; i++)
        {
            if (i >= 1) dp[i] += dp[i - 1];
            if (i >= 2) dp[i] += dp[i - 2];
            if (i >= 3) dp[i] += dp[i - 3];
        }
        
        return dp[n];
    }
}
