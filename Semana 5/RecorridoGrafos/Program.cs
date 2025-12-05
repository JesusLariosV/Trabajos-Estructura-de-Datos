using System;
using System.Collections.Generic;
using System.Linq;

namespace RecorridoGrafos
{
    public enum NodeState
    {
        NotVisited,
        InProcess,
        Completed
    }

    public class GraphTraversal
    {
        private Dictionary<string, List<string>> adjacencyList;
        
        public GraphTraversal()
        {
            adjacencyList = new Dictionary<string, List<string>>();
        }
        
        public void AddEdge(string u, string v)
        {
            if (!adjacencyList.ContainsKey(u))
                adjacencyList[u] = new List<string>();
            if (!adjacencyList.ContainsKey(v))
                adjacencyList[v] = new List<string>();
            
            adjacencyList[u].Add(v);
            adjacencyList[v].Add(u);
        }
        
        public void AddDirectedEdge(string u, string v)
        {
            if (!adjacencyList.ContainsKey(u))
                adjacencyList[u] = new List<string>();
            
            adjacencyList[u].Add(v);
            
            if (!adjacencyList.ContainsKey(v))
                adjacencyList[v] = new List<string>();
        }
        
        // ========================================
        // BUSQUEDA EN AMPLITUD (BFS)
        // ========================================
        
        public List<string> BFS(string start)
        {
            if (!adjacencyList.ContainsKey(start))
                throw new ArgumentException($"El nodo {start} no existe en el grafo");
            
            var visited = new HashSet<string>();
            var result = new List<string>();
            var queue = new Queue<string>();
            
            queue.Enqueue(start);
            visited.Add(start);
            
            while (queue.Count > 0)
            {
                string current = queue.Dequeue();
                result.Add(current);
                
                if (adjacencyList.ContainsKey(current))
                {
                    foreach (string neighbor in adjacencyList[current].OrderBy(x => x))
                    {
                        if (!visited.Contains(neighbor))
                        {
                            visited.Add(neighbor);
                            queue.Enqueue(neighbor);
                        }
                    }
                }
            }
            
            return result;
        }
        
        public Dictionary<string, int> BFSDistances(string start)
        {
            var distances = new Dictionary<string, int>();
            var queue = new Queue<string>();
            
            queue.Enqueue(start);
            distances[start] = 0;
            
            while (queue.Count > 0)
            {
                string current = queue.Dequeue();
                
                if (adjacencyList.ContainsKey(current))
                {
                    foreach (string neighbor in adjacencyList[current])
                    {
                        if (!distances.ContainsKey(neighbor))
                        {
                            distances[neighbor] = distances[current] + 1;
                            queue.Enqueue(neighbor);
                        }
                    }
                }
            }
            
            return distances;
        }
        
        public List<string> BFSShortestPath(string start, string end)
        {
            var parent = new Dictionary<string, string>();
            var visited = new HashSet<string>();
            var queue = new Queue<string>();
            
            queue.Enqueue(start);
            visited.Add(start);
            parent[start] = null;
            
            bool found = false;
            
            while (queue.Count > 0 && !found)
            {
                string current = queue.Dequeue();
                
                if (current == end)
                {
                    found = true;
                    break;
                }
                
                if (adjacencyList.ContainsKey(current))
                {
                    foreach (string neighbor in adjacencyList[current])
                    {
                        if (!visited.Contains(neighbor))
                        {
                            visited.Add(neighbor);
                            parent[neighbor] = current;
                            queue.Enqueue(neighbor);
                        }
                    }
                }
            }
            
            if (!found) return null;
            
            var path = new List<string>();
            string node = end;
            while (node != null)
            {
                path.Add(node);
                node = parent[node];
            }
            
            path.Reverse();
            return path;
        }
        
        // ========================================
        // BUSQUEDA EN PROFUNDIDAD (DFS)
        // ========================================
        
        public List<string> DFSRecursive(string start)
        {
            if (!adjacencyList.ContainsKey(start))
                throw new ArgumentException($"El nodo {start} no existe en el grafo");
            
            var visited = new HashSet<string>();
            var result = new List<string>();
            
            DFSRecursiveHelper(start, visited, result);
            
            return result;
        }
        
        private void DFSRecursiveHelper(string node, HashSet<string> visited, List<string> result)
        {
            visited.Add(node);
            result.Add(node);
            
            if (adjacencyList.ContainsKey(node))
            {
                foreach (string neighbor in adjacencyList[node].OrderBy(x => x))
                {
                    if (!visited.Contains(neighbor))
                    {
                        DFSRecursiveHelper(neighbor, visited, result);
                    }
                }
            }
        }
        
        public List<string> DFSIterative(string start)
        {
            if (!adjacencyList.ContainsKey(start))
                throw new ArgumentException($"El nodo {start} no existe en el grafo");
            
            var visited = new HashSet<string>();
            var result = new List<string>();
            var stack = new Stack<string>();
            
            stack.Push(start);
            
            while (stack.Count > 0)
            {
                string current = stack.Pop();
                
                if (visited.Contains(current))
                    continue;
                
                visited.Add(current);
                result.Add(current);
                
                if (adjacencyList.ContainsKey(current))
                {
                    var neighbors = adjacencyList[current].OrderBy(x => x).Reverse().ToList();
                    
                    foreach (string neighbor in neighbors)
                    {
                        if (!visited.Contains(neighbor))
                        {
                            stack.Push(neighbor);
                        }
                    }
                }
            }
            
            return result;
        }
        
        // ========================================
        // DETECCION DE CICLOS
        // ========================================
        
        public bool HasCycleDirected()
        {
            var state = new Dictionary<string, NodeState>();
            
            foreach (var node in adjacencyList.Keys)
            {
                state[node] = NodeState.NotVisited;
            }
            
            foreach (var node in adjacencyList.Keys)
            {
                if (state[node] == NodeState.NotVisited)
                {
                    if (HasCycleDirectedHelper(node, state))
                        return true;
                }
            }
            
            return false;
        }
        
        private bool HasCycleDirectedHelper(string node, Dictionary<string, NodeState> state)
        {
            state[node] = NodeState.InProcess;
            
            if (adjacencyList.ContainsKey(node))
            {
                foreach (string neighbor in adjacencyList[node])
                {
                    if (state[neighbor] == NodeState.InProcess)
                        return true;
                    
                    if (state[neighbor] == NodeState.NotVisited)
                    {
                        if (HasCycleDirectedHelper(neighbor, state))
                            return true;
                    }
                }
            }
            
            state[node] = NodeState.Completed;
            return false;
        }
    }

    class Program
    {
        static void Main()
        {
            Console.WriteLine("=== Recorrido de Grafos - Semana 5 ===\n");
            
            // Crear grafo de ejemplo del HTML (A-B-C-D-E-F-G)
            var graph = new GraphTraversal();
            graph.AddEdge("A", "B");
            graph.AddEdge("A", "C");
            graph.AddEdge("B", "D");
            graph.AddEdge("B", "E");
            graph.AddEdge("C", "F");
            graph.AddEdge("E", "G");
            
            Console.WriteLine("=== BFS desde A ===");
            var bfsResult = graph.BFS("A");
            Console.WriteLine($"Orden de visita: {string.Join(" -> ", bfsResult)}");
            
            var distances = graph.BFSDistances("A");
            Console.WriteLine("\nDistancias desde A:");
            foreach (var kvp in distances.OrderBy(x => x.Key))
            {
                Console.WriteLine($"  {kvp.Key}: {kvp.Value}");
            }
            
            Console.WriteLine("\n=== DFS Recursivo desde A ===");
            var dfsRecResult = graph.DFSRecursive("A");
            Console.WriteLine($"Orden de visita: {string.Join(" -> ", dfsRecResult)}");
            
            Console.WriteLine("\n=== DFS Iterativo desde A ===");
            var dfsIterResult = graph.DFSIterative("A");
            Console.WriteLine($"Orden de visita: {string.Join(" -> ", dfsIterResult)}");
            
            Console.WriteLine("\n=== Camino mas corto de A a G (BFS) ===");
            var path = graph.BFSShortestPath("A", "G");
            if (path != null)
            {
                Console.WriteLine($"Camino: {string.Join(" -> ", path)}");
                Console.WriteLine($"Longitud: {path.Count - 1} aristas");
            }
            
            // Deteccion de ciclos en grafo dirigido
            Console.WriteLine("\n=== Deteccion de Ciclos ===");
            
            var directedGraph = new GraphTraversal();
            directedGraph.AddDirectedEdge("1", "2");
            directedGraph.AddDirectedEdge("2", "3");
            directedGraph.AddDirectedEdge("3", "1"); // Ciclo: 1->2->3->1
            directedGraph.AddDirectedEdge("3", "4");
            
            bool hasCycle = directedGraph.HasCycleDirected();
            Console.WriteLine($"Grafo dirigido con ciclo: {(hasCycle ? "SI" : "NO")}");
            
            var acyclicGraph = new GraphTraversal();
            acyclicGraph.AddDirectedEdge("1", "2");
            acyclicGraph.AddDirectedEdge("2", "3");
            acyclicGraph.AddDirectedEdge("3", "4");
            
            bool hasCycle2 = acyclicGraph.HasCycleDirected();
            Console.WriteLine($"Grafo dirigido aciclico: {(hasCycle2 ? "SI tiene ciclo" : "NO tiene ciclo")}");
            
            Console.WriteLine("\n=== Proyecto completado exitosamente! ===");
        }
    }
}
