from weighted_graph import WeightedGraph
from typing import Dict, List, Tuple
import math


class RouteOptimizer:
    """
    Optimizador de rutas urbanas usando algoritmos de caminos más cortos.
    """
    
    def __init__(self):
        self.graph: WeightedGraph = None
        self.node_names: Dict[int, str] = {}
        self.traffic_multiplier: Dict[Tuple[int, int], float] = {}
    
    def load_city_network(self, nodes: List[str], edges: List[Tuple[str, str, float]]):
        """
        Carga una red de ciudad.
        
        Args:
            nodes: Lista de nombres de intersecciones
            edges: Lista de tuplas (origen, destino, distancia_km)
        """
        # Crear mapeo de nombres a índices
        self.node_names = {i: name for i, name in enumerate(nodes)}
        name_to_id = {name: i for i, name in enumerate(nodes)}
        
        # Crear grafo
        self.graph = WeightedGraph(len(nodes))
        
        # Agregar aristas (no dirigido para calles)
        for u_name, v_name, weight in edges:
            u = name_to_id[u_name]
            v = name_to_id[v_name]
            self.graph.add_edge(u, v, weight, directed=False)
    
    def set_traffic(self, edge: Tuple[str, str], multiplier: float):
        """
        Establece un multiplicador de tráfico para una arista.
        
        Args:
            edge: Tupla (origen, destino)
            multiplier: Multiplicador de tiempo (1.0 = normal, 2.0 = doble tiempo)
        """
        # Convertir nombres a IDs
        name_to_id = {name: i for i, name in self.node_names.items()}
        u = name_to_id[edge[0]]
        v = name_to_id[edge[1]]
        
        self.traffic_multiplier[(u, v)] = multiplier
        self.traffic_multiplier[(v, u)] = multiplier  # Bidireccional
    
    def optimize_route(self, start: str, end: str, use_traffic: bool = False) -> Tuple[List[str], float]:
        """
        Encuentra la ruta óptima entre dos puntos.
        
        Args:
            start: Nombre del nodo de inicio
            end: Nombre del nodo de destino
            use_traffic: Si se debe considerar el tráfico
            
        Returns:
            Tupla (camino, distancia) donde camino es lista de nombres de nodos
        """
        # Convertir nombres a IDs
        name_to_id = {name: i for i, name in self.node_names.items()}
        start_id = name_to_id[start]
        end_id = name_to_id[end]
        
        # Crear grafo temporal si hay tráfico
        if use_traffic and self.traffic_multiplier:
            temp_graph = WeightedGraph(self.graph.n)
            
            # Copiar aristas con multiplicadores de tráfico
            for u in range(self.graph.n):
                for v, w in self.graph.adj[u]:
                    multiplier = self.traffic_multiplier.get((u, v), 1.0)
                    temp_graph.add_edge(u, v, w * multiplier, directed=True)
            
            dist, parent = temp_graph.dijkstra(start_id)
        else:
            dist, parent = self.graph.dijkstra(start_id)
        
        # Reconstruir camino
        path_ids = self.graph.get_path_dijkstra(parent, start_id, end_id)
        path_names = [self.node_names[i] for i in path_ids]
        
        return path_names, dist[end_id]
    
    def analyze_network(self) -> Dict[str, any]:
        """
        Analiza la red completa usando Floyd-Warshall.
        
        Returns:
            Diccionario con análisis de la red:
            - central_nodes: Nodos más centrales (menor distancia promedio)
            - diameter: Diámetro de la red (máxima distancia entre pares)
            - avg_distance: Distancia promedio entre todos los pares
        """
        dist, parent = self.graph.floyd_warshall()
        
        # Calcular centralidad (distancia promedio desde cada nodo)
        centrality = {}
        for i in range(self.graph.n):
            total_dist = sum(dist[i][j] for j in range(self.graph.n) if i != j and dist[i][j] != math.inf)
            reachable = sum(1 for j in range(self.graph.n) if i != j and dist[i][j] != math.inf)
            avg_dist = total_dist / reachable if reachable > 0 else math.inf
            centrality[self.node_names[i]] = avg_dist
        
        # Encontrar nodos más centrales
        central_nodes = sorted(centrality.items(), key=lambda x: x[1])[:3]
        
        # Calcular diámetro (máxima distancia finita)
        diameter = 0
        for i in range(self.graph.n):
            for j in range(self.graph.n):
                if dist[i][j] != math.inf:
                    diameter = max(diameter, dist[i][j])
        
        # Distancia promedio
        total = 0
        count = 0
        for i in range(self.graph.n):
            for j in range(self.graph.n):
                if i != j and dist[i][j] != math.inf:
                    total += dist[i][j]
                    count += 1
        avg_distance = total / count if count > 0 else 0
        
        return {
            'central_nodes': central_nodes,
            'diameter': diameter,
            'avg_distance': avg_distance,
            'distance_matrix': dist
        }
    
    def simulate_traffic_impact(self, congested_edges: List[Tuple[str, str]], 
                                multiplier: float = 2.0) -> Dict[str, float]:
        """
        Simula el impacto del tráfico en rutas específicas.
        
        Args:
            congested_edges: Lista de aristas congestionadas
            multiplier: Multiplicador de tiempo para aristas congestionadas
            
        Returns:
            Diccionario con impacto en distancia promedio
        """
        # Análisis sin tráfico
        baseline = self.analyze_network()
        
        # Aplicar tráfico
        for edge in congested_edges:
            self.set_traffic(edge, multiplier)
        
        # Análisis con tráfico (crear grafo temporal)
        temp_graph = WeightedGraph(self.graph.n)
        for u in range(self.graph.n):
            for v, w in self.graph.adj[u]:
                mult = self.traffic_multiplier.get((u, v), 1.0)
                temp_graph.add_edge(u, v, w * mult, directed=True)
        
        dist_traffic, _ = temp_graph.floyd_warshall()
        
        # Calcular distancia promedio con tráfico
        total = 0
        count = 0
        for i in range(self.graph.n):
            for j in range(self.graph.n):
                if i != j and dist_traffic[i][j] != math.inf:
                    total += dist_traffic[i][j]
                    count += 1
        avg_with_traffic = total / count if count > 0 else 0
        
        # Limpiar tráfico
        self.traffic_multiplier.clear()
        
        return {
            'baseline_avg': baseline['avg_distance'],
            'traffic_avg': avg_with_traffic,
            'increase_pct': ((avg_with_traffic - baseline['avg_distance']) / baseline['avg_distance'] * 100)
        }


# Ejemplo de uso
if __name__ == "__main__":
    optimizer = RouteOptimizer()
    
    # Definir red de ciudad (ejemplo simplificado)
    nodes = ["Centro", "Norte", "Sur", "Este", "Oeste", "Aeropuerto"]
    edges = [
        ("Centro", "Norte", 5.0),
        ("Centro", "Sur", 4.0),
        ("Centro", "Este", 3.0),
        ("Centro", "Oeste", 3.5),
        ("Norte", "Aeropuerto", 8.0),
        ("Este", "Aeropuerto", 6.0),
        ("Sur", "Oeste", 2.0),
        ("Oeste", "Norte", 7.0)
    ]
    
    optimizer.load_city_network(nodes, edges)
    
    # Optimizar ruta
    print("=== OPTIMIZACIÓN DE RUTA ===")
    path, dist = optimizer.optimize_route("Centro", "Aeropuerto")
    print(f"Ruta óptima: {' -> '.join(path)}")
    print(f"Distancia: {dist:.2f} km")
    
    # Análisis de red
    print("\n=== ANÁLISIS DE RED ===")
    analysis = optimizer.analyze_network()
    print(f"Nodos centrales: {analysis['central_nodes']}")
    print(f"Diámetro de la red: {analysis['diameter']:.2f} km")
    print(f"Distancia promedio: {analysis['avg_distance']:.2f} km")
    
    # Simular tráfico
    print("\n=== IMPACTO DE TRÁFICO ===")
    impact = optimizer.simulate_traffic_impact([("Centro", "Norte"), ("Centro", "Este")])
    print(f"Distancia promedio sin tráfico: {impact['baseline_avg']:.2f} km")
    print(f"Distancia promedio con tráfico: {impact['traffic_avg']:.2f} km")
    print(f"Incremento: {impact['increase_pct']:.1f}%")
