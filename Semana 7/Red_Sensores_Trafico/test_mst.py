import pytest
from mst import GraphMST

def test_mst_simple_connected():
    """Test en un grafo simple conectado."""
    g = GraphMST(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 6)
    g.add_edge(0, 3, 5)
    g.add_edge(1, 3, 15)
    g.add_edge(2, 3, 4)

    # MST esperado: (2,3,4), (0,3,5), (0,1,10) -> Costo 19
    # O alternativamente: (2,3,4), (0,3,5), (0,1,10)
    
    edges_prim, cost_prim = g.prim_mst(0)
    edges_kruskal, cost_kruskal = g.kruskal_mst()
    
    assert cost_prim == 19
    assert cost_kruskal == 19
    assert len(edges_prim) == 3
    assert len(edges_kruskal) == 3

def test_mst_disconnected():
    """Test en un grafo desconectado (bosque)."""
    g = GraphMST(4)
    g.add_edge(0, 1, 5)
    g.add_edge(2, 3, 10)
    
    # Prim solo explorará el componente del nodo inicial
    edges_prim, cost_prim = g.prim_mst(0)
    assert cost_prim == 5
    assert len(edges_prim) == 1
    
    # Kruskal debería encontrar el MST de todos los componentes (MSF - Minimum Spanning Forest)
    edges_kruskal, cost_kruskal = g.kruskal_mst()
    assert cost_kruskal == 15
    assert len(edges_kruskal) == 2

def test_mst_single_node():
    """Test con un solo nodo."""
    g = GraphMST(1)
    
    edges_prim, cost_prim = g.prim_mst(0)
    edges_kruskal, cost_kruskal = g.kruskal_mst()
    
    assert cost_prim == 0
    assert cost_kruskal == 0
    assert len(edges_prim) == 0
    assert len(edges_kruskal) == 0

def test_mst_cycle():
    """Test grafo con ciclo (triángulo equilátero)."""
    g = GraphMST(3)
    g.add_edge(0, 1, 10)
    g.add_edge(1, 2, 10)
    g.add_edge(2, 0, 10)
    
    # MST debe tener 2 aristas de peso 10, costo 20
    _, cost_prim = g.prim_mst(0)
    _, cost_kruskal = g.kruskal_mst()
    
    assert cost_prim == 20
    assert cost_kruskal == 20

def test_mst_duplicate_weights():
    """Test con aristas de igual peso."""
    g = GraphMST(4)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 0, 1) # Ciclo
    
    # MST debe tener 3 aristas de peso 1, costo 3
    _, cost_prim = g.prim_mst(0)
    _, cost_kruskal = g.kruskal_mst()
    
    assert cost_prim == 3
    assert cost_kruskal == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
