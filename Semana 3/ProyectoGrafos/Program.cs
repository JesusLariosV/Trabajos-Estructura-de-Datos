using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class Graph<T> where T : IComparable<T>
{
    private readonly Dictionary<T, List<(T to, double weight)>> adjacencyList = new();
    
    // Agregar un vértice al grafo
    public void AddVertex(T vertex)
    {
        if (!adjacencyList.ContainsKey(vertex))
        {
            adjacencyList[vertex] = new List<(T, double)>();
        }
    }
    
    // Agregar una arista (dirigida o no dirigida)
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
    
    // Exportar a archivo con deduplicación mejorada
    public void ExportToFile(string filename, bool includeWeights = true, bool deduplicateUndirected = false)
    {
        try
        {
            using var writer = new StreamWriter(filename);
            var processedEdges = new HashSet<string>();

            foreach (var vertex in adjacencyList.Keys.OrderBy(v => v))
            {
                foreach (var (neighbor, weight) in adjacencyList[vertex])
                {
                    if (deduplicateUndirected)
                    {
                        // Para grafos no dirigidos, crear clave única ordenada
                        var vertexStr = vertex?.ToString() ?? "";
                        var neighborStr = neighbor?.ToString() ?? "";
                        
                        var edgeKey = vertex.CompareTo(neighbor) <= 0
                            ? $"{vertexStr}→{neighborStr}"
                            : $"{neighborStr}→{vertexStr}";
                        
                        if (!processedEdges.Add(edgeKey))
                            continue; // Saltar si ya fue procesada
                    }
                    
                    // Escribir la arista al archivo
                    var line = includeWeights 
                        ? $"{vertex} {neighbor} {weight:F1}"
                        : $"{vertex} {neighbor}";
                    writer.WriteLine(line);
                }
            }
            Console.WriteLine($"✅ Archivo '{filename}' exportado exitosamente.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error al exportar archivo: {ex.Message}");
        }
    }
    
    public IEnumerable<T> GetVertices() => adjacencyList.Keys;
    
    public IEnumerable<(T neighbor, double weight)> GetNeighbors(T vertex)
    {
        return adjacencyList.TryGetValue(vertex, out var neighbors) 
            ? neighbors 
            : Enumerable.Empty<(T, double)>();
    }
    
    public bool HasEdge(T from, T to)
    {
        return adjacencyList.TryGetValue(from, out var neighbors) && 
               neighbors.Any(edge => EqualityComparer<T>.Default.Equals(edge.to, to));
    }
    
    public int GetOutDegree(T vertex)
    {
        return adjacencyList.TryGetValue(vertex, out var neighbors) ? neighbors.Count : 0;
    }
    
    public int GetInDegree(T vertex)
    {
        return adjacencyList.Values
            .SelectMany(neighbors => neighbors)
            .Count(edge => EqualityComparer<T>.Default.Equals(edge.to, vertex));
    }
    
    public void PrintGraph()
    {
        Console.WriteLine("=== Estructura del Grafo ===");
        foreach (var vertex in adjacencyList.Keys.OrderBy(v => v))
        {
            var neighbors = string.Join(", ", 
                adjacencyList[vertex].Select(edge => $"{edge.to}({edge.weight:F1})"));
            Console.WriteLine($"{vertex}: [{neighbors}]");
        }
    }
}

// Programa principal con el mapa de la ciudad
class Program
{
    static void Main()
    {
        Console.WriteLine("🌍 === Generando Mapa de Tráfico === 🌍");

        // Grafo No Dirigido (calles bidireccionales)
        var undirected = new Graph<string>();
        Console.WriteLine("\n🛣️ Agregando calles bidireccionales...");
        
        undirected.AddEdge("A", "B", 2.0, false);
        undirected.AddEdge("A", "C", 3.0, false);
        undirected.AddEdge("B", "D", 1.0, false);
        undirected.AddEdge("C", "E", 4.0, false);
        undirected.AddEdge("D", "F", 5.0, false);
        undirected.AddEdge("E", "F", 2.0, false);
        undirected.AddEdge("G", "H", 6.0, false);
        
        undirected.ExportToFile("edges_undirected.txt", includeWeights: true, deduplicateUndirected: true);

        // Grafo Dirigido (todas las aristas)
        var directed = new Graph<string>();
        Console.WriteLine("\n🚦 Creando mapa completo con calles direccionales...");
        
        // Aristas dirigidas específicas
        directed.AddEdge("A", "G", 1.0, true);
        directed.AddEdge("B", "H", 3.0, true);
        directed.AddEdge("C", "D", 2.0, true);
        directed.AddEdge("F", "E", 4.0, true);
        directed.AddEdge("H", "A", 5.0, true);
        
        // Agregar también las bidireccionales como dirigidas (ida y vuelta)
        directed.AddEdge("A", "B", 2.0, true);
        directed.AddEdge("B", "A", 2.0, true);
        directed.AddEdge("A", "C", 3.0, true);
        directed.AddEdge("C", "A", 3.0, true);
        directed.AddEdge("B", "D", 1.0, true);
        directed.AddEdge("D", "B", 1.0, true);
        directed.AddEdge("C", "E", 4.0, true);
        directed.AddEdge("E", "C", 4.0, true);
        directed.AddEdge("D", "F", 5.0, true);
        directed.AddEdge("F", "D", 5.0, true);
        directed.AddEdge("E", "F", 2.0, true);
        directed.AddEdge("F", "E", 2.0, true);
        directed.AddEdge("G", "H", 6.0, true);
        directed.AddEdge("H", "G", 6.0, true);
        
        directed.ExportToFile("edges_directed.txt", includeWeights: true, deduplicateUndirected: false);

        // Pruebas de funcionalidad
        Console.WriteLine("\n🧪 === Pruebas de Funcionalidad ===");
        Console.WriteLine($"Grado de A (no dirigido): {undirected.GetOutDegree("A")} (esperado: 2)");
        Console.WriteLine($"¿Existe A↔B no dirigido? {undirected.HasEdge("A", "B")} (esperado: True)");
        Console.WriteLine($"¿Existe B↔A no dirigido? {undirected.HasEdge("B", "A")} (esperado: True)");
        
        Console.WriteLine($"\nGrado salida A (dirigido): {directed.GetOutDegree("A")}");
        Console.WriteLine($"Grado entrada A (dirigido): {directed.GetInDegree("A")}");
        Console.WriteLine($"¿Existe A→G dirigido? {directed.HasEdge("A", "G")} (esperado: True)");
        Console.WriteLine($"¿Existe G→A dirigido? {directed.HasEdge("G", "A")} (esperado: False)");
        
        Console.WriteLine("\n🎉 ¡Proyecto C# completado exitosamente!");
    }
}
