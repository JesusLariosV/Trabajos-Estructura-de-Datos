from collections import deque, defaultdict
from typing import List, Dict, Set
from enum import Enum

class NodeState(Enum):
    NOT_VISITED = 0
    IN_PROCESS = 1
    COMPLETED = 2

class GraphTraversal:
    def __init__(self):
        self.adjacency_list = defaultdict(list)
    
    def add_edge(self, u: str, v: str):
        """Add undirected edge"""
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)
    
    def add_directed_edge(self, u: str, v: str):
        """Add directed edge"""
        self.adjacency_list[u].append(v)
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
    
    # ========================================
    # BUSQUEDA EN AMPLITUD (BFS)
    # ========================================
    
    def bfs(self, start: str) -> List[str]:
        """BFS traversal returning visit order"""
        if start not in self.adjacency_list:
            raise ValueError(f"El nodo {start} no existe en el grafo")
        
        visited = set()
        result = []
        queue = deque()
        
        queue.append(start)
        visited.add(start)
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            if current in self.adjacency_list:
                for neighbor in sorted(self.adjacency_list[current]):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        
        return result
    
    def bfs_distances(self, start: str) -> Dict[str, int]:
        """BFS returning distances from start node"""
        distances = {}
        queue = deque()
        
        queue.append(start)
        distances[start] = 0
        
        while queue:
            current = queue.popleft()
            
            if current in self.adjacency_list:
                for neighbor in self.adjacency_list[current]:
                    if neighbor not in distances:
                        distances[neighbor] = distances[current] + 1
                        queue.append(neighbor)
        
        return distances
    
    def bfs_shortest_path(self, start: str, end: str) -> List[str]:
        """BFS finding shortest path"""
        parent = {}
        visited = set()
        queue = deque()
        
        queue.append(start)
        visited.add(start)
        parent[start] = None
        
        found = False
        
        while queue and not found:
            current = queue.popleft()
            
            if current == end:
                found = True
                break
            
            if current in self.adjacency_list:
                for neighbor in self.adjacency_list[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        parent[neighbor] = current
                        queue.append(neighbor)
        
        if not found:
            return None
        
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = parent[node]
        
        path.reverse()
        return path
    
    # ========================================
    # BUSQUEDA EN PROFUNDIDAD (DFS)
    # ========================================
    
    def dfs_recursive(self, start: str) -> List[str]:
        """DFS recursive traversal"""
        if start not in self.adjacency_list:
            raise ValueError(f"El nodo {start} no existe en el grafo")
        
        visited = set()
        result = []
        
        self._dfs_recursive_helper(start, visited, result)
        
        return result
    
    def _dfs_recursive_helper(self, node: str, visited: Set[str], result: List[str]):
        """Helper for recursive DFS"""
        visited.add(node)
        result.append(node)
        
        if node in self.adjacency_list:
            for neighbor in sorted(self.adjacency_list[node]):
                if neighbor not in visited:
                    self._dfs_recursive_helper(neighbor, visited, result)
    
    def dfs_iterative(self, start: str) -> List[str]:
        """DFS iterative traversal using explicit stack"""
        if start not in self.adjacency_list:
            raise ValueError(f"El nodo {start} no existe en el grafo")
        
        visited = set()
        result = []
        stack = []
        
        stack.append(start)
        
        while stack:
            current = stack.pop()
            
            if current in visited:
                continue
            
            visited.add(current)
            result.append(current)
            
            if current in self.adjacency_list:
                neighbors = sorted(self.adjacency_list[current], reverse=True)
                
                for neighbor in neighbors:
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    # ========================================
    # DETECCION DE CICLOS
    # ========================================
    
    def has_cycle_directed(self) -> bool:
        """Detect cycle in directed graph using DFS"""
        state = {node: NodeState.NOT_VISITED for node in self.adjacency_list.keys()}
        
        for node in self.adjacency_list.keys():
            if state[node] == NodeState.NOT_VISITED:
                if self._has_cycle_directed_helper(node, state):
                    return True
        
        return False
    
    def _has_cycle_directed_helper(self, node: str, state: Dict[str, NodeState]) -> bool:
        """Helper for cycle detection"""
        state[node] = NodeState.IN_PROCESS
        
        if node in self.adjacency_list:
            for neighbor in self.adjacency_list[node]:
                if state[neighbor] == NodeState.IN_PROCESS:
                    return True
                
                if state[neighbor] == NodeState.NOT_VISITED:
                    if self._has_cycle_directed_helper(neighbor, state):
                        return True
        
        state[node] = NodeState.COMPLETED
        return False

def main():
    print("=== Recorrido de Grafos - Semana 5 (Python) ===\n")
    
    # Crear grafo de ejemplo del HTML (A-B-C-D-E-F-G)
    graph = GraphTraversal()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("B", "E")
    graph.add_edge("C", "F")
    graph.add_edge("E", "G")
    
    print("=== BFS desde A ===")
    bfs_result = graph.bfs("A")
    print(f"Orden de visita: {' -> '.join(bfs_result)}")
    
    distances = graph.bfs_distances("A")
    print("\nDistancias desde A:")
    for node in sorted(distances.keys()):
        print(f"  {node}: {distances[node]}")
    
    print("\n=== DFS Recursivo desde A ===")
    dfs_rec_result = graph.dfs_recursive("A")
    print(f"Orden de visita: {' -> '.join(dfs_rec_result)}")
    
    print("\n=== DFS Iterativo desde A ===")
    dfs_iter_result = graph.dfs_iterative("A")
    print(f"Orden de visita: {' -> '.join(dfs_iter_result)}")
    
    print("\n=== Camino mas corto de A a G (BFS) ===")
    path = graph.bfs_shortest_path("A", "G")
    if path:
        print(f"Camino: {' -> '.join(path)}")
        print(f"Longitud: {len(path) - 1} aristas")
    
    # Deteccion de ciclos en grafo dirigido
    print("\n=== Deteccion de Ciclos ===")
    
    directed_graph = GraphTraversal()
    directed_graph.add_directed_edge("1", "2")
    directed_graph.add_directed_edge("2", "3")
    directed_graph.add_directed_edge("3", "1")  # Ciclo: 1->2->3->1
    directed_graph.add_directed_edge("3", "4")
    
    has_cycle = directed_graph.has_cycle_directed()
    print(f"Grafo dirigido con ciclo: {'SI' if has_cycle else 'NO'}")
    
    acyclic_graph = GraphTraversal()
    acyclic_graph.add_directed_edge("1", "2")
    acyclic_graph.add_directed_edge("2", "3")
    acyclic_graph.add_directed_edge("3", "4")
    
    has_cycle2 = acyclic_graph.has_cycle_directed()
    print(f"Grafo dirigido aciclico: {'SI tiene ciclo' if has_cycle2 else 'NO tiene ciclo'}")
    
    print("\n=== Proyecto completado exitosamente! ===")

if __name__ == "__main__":
    main()
