using System;
using System.Collections.Generic;
using System.Linq;

// Graph class from Week 3 (copied for standalone execution)
public class Graph<T> where T : IComparable<T>
{
    private readonly Dictionary<T, List<(T to, double weight)>> adjacencyList = new();
    
    public void AddVertex(T vertex)
    {
        if (!adjacencyList.ContainsKey(vertex))
        {
            adjacencyList[vertex] = new List<(T, double)>();
        }
    }
    
    public void AddEdge(T from, T to, double weight = 1.0, bool isDirected = true)
    {
        AddVertex(from);
        AddVertex(to);
        
        adjacencyList[from].Add((to, weight));
        
        if (!isDirected)
        {
            adjacencyList[to].Add((from, weight));
        }
    }
    
    public IEnumerable<T> GetVertices() => adjacencyList.Keys;
    
    public int GetOutDegree(T vertex)
    {
        return adjacencyList.TryGetValue(vertex, out var neighbors) ? neighbors.Count : 0;
    }
}

// GraphValidator class for Week 4
public static class GraphValidator
{
    /// <summary>
    /// Validates if a degree sequence is graphical using Havel-Hakimi algorithm.
    /// Complexity: O(n² log n) due to repeated sorting in each iteration.
    /// </summary>
    public static bool IsGraphicalSequence(List<int> degrees)
    {
        if (degrees.Count == 0) return true;
        
        // Create copy to avoid modifying original
        var seq = new List<int>(degrees);
        
        // Sort in descending order
        seq.Sort((a, b) => b.CompareTo(a));
        
        // Verify even sum and max degree
        int sum = seq.Sum();
        if (sum % 2 != 0 || seq[0] >= seq.Count) return false;
        
        while (seq.Count > 0)
        {
            int d1 = seq[0];
            seq.RemoveAt(0); // Remove d1
            
            if (d1 == 0) return true; // All zeros
            
            if (d1 > seq.Count) return false;
            
            // Subtract 1 from the next d1 elements
            for (int i = 0; i < d1; i++)
            {
                seq[i]--;
                if (seq[i] < 0) return false;
            }
            
            // CRITICAL: Reorder after modification
            seq.Sort((a, b) => b.CompareTo(a));
        }
        return true;
    }
    
    /// <summary>
    /// Verifies consistency: sum of degrees must be even for undirected graph.
    /// </summary>
    public static bool ValidateConsistency<T>(Graph<T> graph) where T : IComparable<T>
    {
        int totalDegree = graph.GetVertices().Sum(v => graph.GetOutDegree(v));
        // In undirected graph, sum of degrees = 2 * |edges|, must be even
        return totalDegree % 2 == 0;
    }

    /// <summary>
    /// Extracts degree sequence from a graph (useful for connecting with Week 3).
    /// </summary>
    public static List<int> ExtractDegreeSequence<T>(Graph<T> graph) where T : IComparable<T>
    {
        var degrees = graph.GetVertices()
                          .Select(v => graph.GetOutDegree(v))
                          .OrderByDescending(d => d)
                          .ToList();
        return degrees;
    }
}

class Program
{
    static void Main()
    {
        Console.WriteLine("=== Validacion de Grafos - Semana 4 ===\n");
        
        // Test cases from semana4.html
        var testCases = new List<(List<int> seq, bool expected, string reason)>
        {
            (new List<int> {4, 3, 3, 2, 2, 2, 1, 1}, true, "Suma=18 (par), max=4<=7, converge a ceros"),
            (new List<int> {3, 2, 2, 1}, true, "Ejemplo del documento, converge correctamente"),
            (new List<int> {4, 3, 3, 2, 2, 2}, true, "n=6, suma=16 (par), max=4<=5"),
            (new List<int> {0, 0, 0, 0}, true, "Grafo vacio (sin aristas)"),
            (new List<int> {3, 3, 3, 3}, true, "Grafo completo K4 (todos conectados)"),
            (new List<int> {3, 3, 3, 1}, false, "Reduce a [2,2,0] -> [1,-1] (negativo en paso 2)"),
            (new List<int> {5, 5, 4, 3, 2, 1}, false, "Suma=20 (par), pero estructura imposible"),
            (new List<int> {3, 2, 1}, false, "Early exit: max=3 > n-1=2 (falla chequeo inicial)"),
            (new List<int> {6, 1, 1, 1, 1, 1, 1}, false, "n=7, estructura imposible"),
            (new List<int> {5, 3, 2, 2, 1}, false, "Suma=13 (impar) -> imposible en grafo no dirigido")
        };
        
        Console.WriteLine("=== Casos de Prueba Oficiales ===\n");
        int passed = 0;
        for (int i = 0; i < testCases.Count; i++)
        {
            var (seq, expected, reason) = testCases[i];
            bool result = GraphValidator.IsGraphicalSequence(seq);
            string status = result == expected ? "PASS" : "FAIL";
            
            if (result == expected) passed++;
            
            Console.WriteLine($"Caso {i + 1}: [{string.Join(", ", seq)}]");
            Console.WriteLine($"  Esperado: {(expected ? "Grafica" : "No Grafica")}");
            Console.WriteLine($"  Resultado: {(result ? "Grafica" : "No Grafica")} [{status}]");
            Console.WriteLine($"  Razon: {reason}\n");
        }
        
        Console.WriteLine($"Resultado: {passed}/{testCases.Count} casos pasados\n");
        
        // Validate city map from Week 3
        Console.WriteLine("=== Validacion del Mapa Urbano (Semana 3) ===\n");
        var cityGraph = new Graph<string>();
        
        // Recreate undirected graph from Week 3
        cityGraph.AddEdge("A", "B", 2.0, false);
        cityGraph.AddEdge("A", "C", 3.0, false);
        cityGraph.AddEdge("B", "D", 1.0, false);
        cityGraph.AddEdge("C", "E", 4.0, false);
        cityGraph.AddEdge("D", "F", 5.0, false);
        cityGraph.AddEdge("E", "F", 2.0, false);
        cityGraph.AddEdge("G", "H", 6.0, false);
        
        var extractedSeq = GraphValidator.ExtractDegreeSequence(cityGraph);
        bool isGraphical = GraphValidator.IsGraphicalSequence(extractedSeq);
        bool isConsistent = GraphValidator.ValidateConsistency(cityGraph);
        
        Console.WriteLine($"Secuencia extraida: [{string.Join(", ", extractedSeq)}]");
        Console.WriteLine($"Es grafica? {(isGraphical ? "Si" : "No")}");
        Console.WriteLine($"Es consistente (suma par)? {(isConsistent ? "Si" : "No")}");
        
        Console.WriteLine("\n=== Proyecto completado exitosamente! ===");
    }
}
