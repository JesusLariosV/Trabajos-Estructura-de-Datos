from collections import defaultdict
from typing import Dict, List, Tuple
import os

def load_graph(file_path: str, is_directed: bool = True) -> Dict[str, List[Tuple[str, float]]]:
    """
    Carga un grafo desde un archivo de texto con manejo robusto de errores.
    """
    adjacency_list = defaultdict(list)
    
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo '{file_path}' no existe.")
        return adjacency_list
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                # Ignorar líneas vacías y comentarios
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) < 2:
                    print(f"⚠️  Línea {line_num}: '{line}' ignorada (faltan vértices)")
                    continue
                
                from_vertex, to_vertex = parts[0], parts[1]
                
                # Procesar peso con validación
                try:
                    weight = float(parts[2]) if len(parts) > 2 else 1.0
                except (ValueError, IndexError):
                    print(f"⚠️  Línea {line_num}: peso inválido, usando 1.0")
                    weight = 1.0
                
                # Agregar arista
                adjacency_list[from_vertex].append((to_vertex, weight))
                
                # Si es no dirigido, agregar arista inversa
                if not is_directed:
                    adjacency_list[to_vertex].append((from_vertex, weight))
                    
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{file_path}'")
    except Exception as e:
        print(f"❌ Error inesperado al leer '{file_path}': {e}")
    
    return dict(adjacency_list)

def get_neighbors(graph: Dict[str, List[Tuple[str, float]]], vertex: str) -> List[Tuple[str, float]]:
    """Obtiene la lista de vecinos de un vértice."""
    return graph.get(vertex, [])

def get_out_degree(graph: Dict[str, List[Tuple[str, float]]], vertex: str) -> int:
    """Calcula el grado de salida de un vértice."""
    return len(graph.get(vertex, []))

def get_in_degree(graph: Dict[str, List[Tuple[str, float]]], vertex: str) -> int:
    """Calcula el grado de entrada de un vértice."""
    in_degree = 0
    for neighbors in graph.values():
        in_degree += sum(1 for neighbor, _ in neighbors if neighbor == vertex)
    return in_degree

def analyze_graph(graph: Dict[str, List[Tuple[str, float]]], graph_type: str):
    """Analiza y muestra estadísticas detalladas del grafo."""
    print(f"\n{'='*50}")
    print(f" Analisis del Grafo {graph_type}")
    print(f"{'='*50}")
    
    if not graph:
        print("  El grafo esta vacio")
        return
    
    vertices = sorted(graph.keys())
    total_edges = sum(len(neighbors) for neighbors in graph.values())
    
    print(f" Estadisticas generales:")
    print(f"   - Vertices: {len(vertices)}")
    print(f"   - Aristas: {total_edges}")
    
    # Calcular densidad (para grafos dirigidos)
    max_possible_edges = len(vertices) * (len(vertices) - 1)
    if max_possible_edges > 0:
        density = total_edges / max_possible_edges
        print(f"   - Densidad: {density:.3f}")
    
    print(f"\n Detalles por vertice:")
    for vertex in vertices:
        out_deg = get_out_degree(graph, vertex)
        in_deg = get_in_degree(graph, vertex)
        neighbors = get_neighbors(graph, vertex)
        
        neighbor_str = ", ".join([f"{neighbor}({weight:.1f}km)" for neighbor, weight in neighbors])
        
        print(f"   {vertex}: Out-degree={out_deg}, In-degree={in_deg}")
        print(f"      - Vecinos: [{neighbor_str}]")

def main():
    print(" === Analisis de Grafos en Python === ")
    
    # Analizar Grafo No Dirigido (cargado como dirigido para ver estructura cruda, o como no dirigido si el archivo solo tiene una dirección)
    # Nota: El archivo exportado por C# para no dirigido ya tiene las aristas deduplicadas (solo una dirección).
    # Por lo tanto, debemos cargarlo con is_directed=False para reconstruir las aristas inversas en memoria.
    undirected_graph = load_graph("edges_undirected.txt", is_directed=False)
    analyze_graph(undirected_graph, "No Dirigido (Calles Bidireccionales)")
    
    # Analizar Grafo Dirigido
    directed_graph = load_graph("edges_directed.txt", is_directed=True)
    analyze_graph(directed_graph, "Dirigido (Mapa Completo)")

if __name__ == "__main__":
    main()
