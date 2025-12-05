import heapq
from typing import List, Tuple, Dict, Set

class GraphMST:
    """
    Clase para manejar grafos y encontrar Árboles de Expansión Mínima (MST).
    Implementa los algoritmos de Prim y Kruskal.
    """
    
    def __init__(self, vertices: int):
        """
        Inicializa el grafo.
        
        Args:
            vertices: Número de vértices (0 a vertices-1)
        """
        self.V = vertices
        self.edges: List[Tuple[int, int, float]] = []  # Para Kruskal: (u, v, w)
        self.adj: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(vertices)}  # Para Prim

    def add_edge(self, u: int, v: int, w: float):
        """
        Agrega una arista no dirigida al grafo.
        
        Args:
            u: Vértice origen
            v: Vértice destino
            w: Peso de la arista
        """
        self.edges.append((u, v, w))
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    # --- ALGORITMO DE PRIM ---
    def prim_mst(self, start_node: int = 0) -> Tuple[List[Tuple[int, int, float]], float]:
        """
        Encuentra el MST usando el algoritmo de Prim.
        Ideal para grafos densos.
        
        Args:
            start_node: Nodo inicial para comenzar el árbol
            
        Returns:
            Tupla (lista de aristas del MST, costo total)
        """
        visited = [False] * self.V
        pq = []  # Priority Queue: (peso, u, v)
        
        # Iniciar con el nodo start_node
        visited[start_node] = True
        for neighbor, weight in self.adj[start_node]:
            heapq.heappush(pq, (weight, start_node, neighbor))
            
        mst_edges = []
        mst_cost = 0
        edges_count = 0
        
        while pq and edges_count < self.V - 1:
            weight, u, v = heapq.heappop(pq)
            
            if visited[v]:
                continue
                
            visited[v] = True
            mst_edges.append((u, v, weight))
            mst_cost += weight
            edges_count += 1
            
            for next_node, next_weight in self.adj[v]:
                if not visited[next_node]:
                    heapq.heappush(pq, (next_weight, v, next_node))
                    
        return mst_edges, mst_cost

    # --- UNION-FIND OPTIMIZADO (DSU) ---
    class DSU:
        """Estructura de datos Disjoint Set Union con optimizaciones."""
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [0] * n

        def find(self, i):
            """Encuentra el representante del conjunto con Path Compression."""
            if self.parent[i] != i:
                self.parent[i] = self.find(self.parent[i])
            return self.parent[i]

        def union(self, i, j):
            """Une dos conjuntos con Union by Rank."""
            root_i = self.find(i)
            root_j = self.find(j)
            
            if root_i != root_j:
                if self.rank[root_i] < self.rank[root_j]:
                    self.parent[root_i] = root_j
                elif self.rank[root_i] > self.rank[root_j]:
                    self.parent[root_j] = root_i
                else:
                    self.parent[root_j] = root_i
                    self.rank[root_i] += 1
                return True
            return False

    # --- ALGORITMO DE KRUSKAL ---
    def kruskal_mst(self) -> Tuple[List[Tuple[int, int, float]], float]:
        """
        Encuentra el MST usando el algoritmo de Kruskal.
        Ideal para grafos dispersos.
        
        Returns:
            Tupla (lista de aristas del MST, costo total)
        """
        mst_cost = 0
        mst_edges = []
        dsu = self.DSU(self.V)

        # Ordenar aristas por peso
        sorted_edges = sorted(self.edges, key=lambda item: item[2])

        for u, v, w in sorted_edges:
            if dsu.union(u, v):
                mst_edges.append((u, v, w))
                mst_cost += w
                
        return mst_edges, mst_cost

# Ejemplo de uso
if __name__ == "__main__":
    g = GraphMST(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 6)
    g.add_edge(0, 3, 5)
    g.add_edge(1, 3, 15)
    g.add_edge(2, 3, 4)

    print("Prim MST:")
    edges_prim, cost_prim = g.prim_mst()
    print(f"Aristas: {edges_prim}")
    print(f"Costo: {cost_prim}")

    print("\nKruskal MST:")
    edges_kruskal, cost_kruskal = g.kruskal_mst()
    print(f"Aristas: {edges_kruskal}")
    print(f"Costo: {cost_kruskal}")
