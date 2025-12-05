import heapq
import math
from typing import Dict, List, Tuple, Optional


class WeightedGraph:
    """
    Grafo ponderado para algoritmos de caminos más cortos.
    Soporta Dijkstra y Floyd-Warshall.
    """
    
    def __init__(self, n: int):
        """
        Inicializa un grafo con n nodos.
        
        Args:
            n: Número de nodos (0 a n-1)
        """
        self.n = n
        self.adj: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(n)}
    
    def add_edge(self, u: int, v: int, w: float, directed: bool = True):
        """
        Agrega una arista al grafo.
        
        Args:
            u: Nodo origen
            v: Nodo destino
            w: Peso de la arista
            directed: Si es dirigido (True) o no dirigido (False)
        """
        self.adj[u].append((v, w))
        if not directed:
            self.adj[v].append((u, w))
    
    def dijkstra(self, src: int) -> Tuple[List[float], List[int]]:
        """
        Algoritmo de Dijkstra para caminos más cortos desde un origen único.
        
        Args:
            src: Nodo origen
            
        Returns:
            Tupla (distancias, padres) donde:
            - distancias[i] es la distancia mínima de src a i
            - padres[i] es el nodo previo en el camino más corto a i
        """
        dist = [math.inf] * self.n
        parent = [-1] * self.n
        dist[src] = 0
        
        # Cola de prioridad: (distancia, nodo)
        pq = [(0, src)]
        visited = [False] * self.n
        
        while pq:
            cost, u = heapq.heappop(pq)
            
            if visited[u]:
                continue
                
            visited[u] = True
            
            # Relajación de aristas
            for v, w in self.adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
        
        return dist, parent
    
    def floyd_warshall(self) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
        """
        Algoritmo de Floyd-Warshall para caminos más cortos entre todos los pares.
        
        Returns:
            Tupla (matriz_distancias, matriz_padres) donde:
            - matriz_distancias[i][j] es la distancia mínima de i a j
            - matriz_padres[i][j] es el nodo previo en el camino de i a j
            
        Raises:
            ValueError: Si se detecta un ciclo negativo
        """
        # Inicializar matriz de distancias
        dist = [[math.inf] * self.n for _ in range(self.n)]
        parent = [[None] * self.n for _ in range(self.n)]
        
        # Distancia de un nodo a sí mismo es 0
        for i in range(self.n):
            dist[i][i] = 0
        
        # Inicializar con aristas directas
        for u in range(self.n):
            for v, w in self.adj[u]:
                dist[u][v] = w
                parent[u][v] = u
        
        # Algoritmo de Floyd-Warshall
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        parent[i][j] = parent[k][j]
        
        # Detectar ciclos negativos
        for i in range(self.n):
            if dist[i][i] < 0:
                raise ValueError(f"Ciclo negativo detectado en nodo {i}")
        
        return dist, parent
    
    def get_path_dijkstra(self, parent: List[int], src: int, dest: int) -> List[int]:
        """
        Reconstruye el camino desde src hasta dest usando el array de padres de Dijkstra.
        
        Args:
            parent: Array de padres de Dijkstra
            src: Nodo origen
            dest: Nodo destino
            
        Returns:
            Lista de nodos en el camino de src a dest (vacía si no hay camino)
        """
        if parent[dest] == -1 and src != dest:
            return []  # No hay camino
        
        path = []
        current = dest
        
        while current != -1:
            path.append(current)
            if current == src:
                break
            current = parent[current]
        
        path.reverse()
        return path if path[0] == src else []
    
    def get_path_floyd_warshall(self, parent: List[List[Optional[int]]], 
                                src: int, dest: int) -> List[int]:
        """
        Reconstruye el camino desde src hasta dest usando la matriz de padres de Floyd-Warshall.
        
        Args:
            parent: Matriz de padres de Floyd-Warshall
            src: Nodo origen
            dest: Nodo destino
            
        Returns:
            Lista de nodos en el camino de src a dest (vacía si no hay camino)
        """
        if parent[src][dest] is None:
            return [] if src != dest else [src]
        
        path = []
        current = dest
        
        while current != src:
            path.append(current)
            current = parent[src][current]
            if current is None:
                return []  # No hay camino
        
        path.append(src)
        path.reverse()
        return path


# Ejemplo de uso
if __name__ == "__main__":
    # Crear grafo de ejemplo (6 nodos)
    g = WeightedGraph(6)
    
    # Agregar aristas (grafo dirigido)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 5)
    g.add_edge(1, 3, 3)
    g.add_edge(2, 3, 2)
    g.add_edge(2, 4, 8)
    g.add_edge(3, 4, 4)
    g.add_edge(1, 5, 15)
    g.add_edge(4, 5, 7)
    
    print("=== DIJKSTRA ===")
    dist, parent = g.dijkstra(0)
    print(f"Distancias desde nodo 0: {dist}")
    print(f"Camino a nodo 5: {g.get_path_dijkstra(parent, 0, 5)}")
    print(f"Distancia a nodo 5: {dist[5]}")
    
    print("\n=== FLOYD-WARSHALL ===")
    fw_dist, fw_parent = g.floyd_warshall()
    print(f"Distancia de 0 a 5: {fw_dist[0][5]}")
    print(f"Camino de 0 a 5: {g.get_path_floyd_warshall(fw_parent, 0, 5)}")
