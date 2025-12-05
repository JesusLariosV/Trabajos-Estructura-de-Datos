import pytest
import math
from weighted_graph import WeightedGraph


def test_dijkstra_simple():
    """Test Dijkstra en grafo simple."""
    g = WeightedGraph(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 5)
    g.add_edge(2, 3, 2)
    g.add_edge(1, 3, 3)
    
    dist, parent = g.dijkstra(0)
    
    assert dist[3] == 7  # 0 -> 2 -> 3
    assert not math.isinf(dist[3])
    
    path = g.get_path_dijkstra(parent, 0, 3)
    assert path == [0, 2, 3]


def test_dijkstra_zero_weight():
    """Test Dijkstra con aristas de peso cero."""
    g = WeightedGraph(3)
    g.add_edge(0, 1, 0)
    g.add_edge(1, 2, 5)
    
    dist, _ = g.dijkstra(0)
    
    assert dist[2] == 5


def test_dijkstra_disconnected():
    """Test Dijkstra en grafo desconectado."""
    g = WeightedGraph(3)
    g.add_edge(0, 1, 10)
    
    dist, _ = g.dijkstra(0)
    
    assert math.isinf(dist[2])


def test_dijkstra_single_node():
    """Test Dijkstra con un solo nodo."""
    g = WeightedGraph(1)
    
    dist, _ = g.dijkstra(0)
    
    assert dist[0] == 0


def test_dijkstra_multiple_paths():
    """Test Dijkstra con múltiples caminos posibles."""
    g = WeightedGraph(4)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 2)
    g.add_edge(1, 3, 1)
    g.add_edge(2, 3, 3)
    
    dist, parent = g.dijkstra(0)
    
    # Camino óptimo: 0 -> 2 -> 3 (costo 5) NO, es 0 -> 1 -> 3 (costo 5)
    # Espera, 0->1 = 4, 1->3 = 1, total = 5
    # 0->2 = 2, 2->3 = 3, total = 5
    # Ambos son iguales, pero Dijkstra elegirá uno
    assert dist[3] == 5


def test_floyd_warshall_simple():
    """Test Floyd-Warshall en grafo simple."""
    g = WeightedGraph(3)
    g.add_edge(0, 1, 4)
    g.add_edge(1, 2, 2)
    g.add_edge(2, 0, 3)
    
    fw, parent = g.floyd_warshall()
    
    assert fw[0][2] == 6  # 0 -> 1 -> 2


def test_floyd_warshall_negative_no_cycle():
    """Test Floyd-Warshall con pesos negativos sin ciclo."""
    g = WeightedGraph(3)
    g.add_edge(0, 1, 2)
    g.add_edge(1, 2, -1)
    
    fw, _ = g.floyd_warshall()
    
    assert fw[0][2] == 1


def test_floyd_warshall_negative_cycle():
    """Test Floyd-Warshall detecta ciclo negativo."""
    g = WeightedGraph(2)
    g.add_edge(0, 1, -2)
    g.add_edge(1, 0, -1)
    
    with pytest.raises(ValueError, match="Ciclo negativo"):
        g.floyd_warshall()


def test_floyd_warshall_disconnected():
    """Test Floyd-Warshall en grafo desconectado."""
    g = WeightedGraph(3)
    g.add_edge(0, 1, 10)
    
    fw, _ = g.floyd_warshall()
    
    assert math.isinf(fw[0][2])


def test_path_reconstruction_dijkstra():
    """Test reconstrucción de camino con Dijkstra."""
    g = WeightedGraph(5)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 4, 1)
    
    dist, parent = g.dijkstra(0)
    path = g.get_path_dijkstra(parent, 0, 4)
    
    assert path == [0, 1, 2, 3, 4]
    assert dist[4] == 4


def test_path_reconstruction_floyd_warshall():
    """Test reconstrucción de camino con Floyd-Warshall."""
    g = WeightedGraph(4)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 1)
    
    fw, parent = g.floyd_warshall()
    path = g.get_path_floyd_warshall(parent, 0, 3)
    
    assert path == [0, 1, 2, 3]
    assert fw[0][3] == 3


def test_undirected_graph():
    """Test grafo no dirigido."""
    g = WeightedGraph(3)
    g.add_edge(0, 1, 5, directed=False)
    g.add_edge(1, 2, 3, directed=False)
    
    dist, _ = g.dijkstra(0)
    
    # Debe poder ir de 0 a 2 y viceversa
    assert dist[2] == 8
    
    dist_reverse, _ = g.dijkstra(2)
    assert dist_reverse[0] == 8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
