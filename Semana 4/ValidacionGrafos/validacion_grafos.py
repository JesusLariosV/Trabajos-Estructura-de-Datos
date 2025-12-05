from typing import List, Dict, Tuple

def is_graphical_sequence(degrees: List[int]) -> bool:
    """
    Validates graphical sequence using Havel-Hakimi algorithm.
    Complexity: O(n² log n) due to reordering in each iteration.
    """
    if not degrees:
        return True
    
    # Create copy to avoid modifying original
    seq = sorted(degrees, reverse=True)
    
    # Verify even sum and max degree
    total_sum = sum(seq)
    if total_sum % 2 != 0 or seq[0] >= len(seq):
        return False
    
    while seq:
        d1 = seq.pop(0)
        
        if d1 == 0:
            return True
        
        if d1 > len(seq):
            return False
        
        # Subtract 1 from the next d1 elements
        for i in range(d1):
            seq[i] -= 1
            if seq[i] < 0:
                return False
        
        # CRITICAL: Reorder after modification
        seq.sort(reverse=True)
    
    return True

def validate_consistency(adjacency_list: Dict[str, List[Tuple[str, float]]]) -> bool:
    """
    Verifies consistency: sum of degrees must be even in undirected graph.
    """
    total_degree = sum(len(neighbors) for neighbors in adjacency_list.values())
    # In undirected graph, sum of degrees = 2 * |edges|
    return total_degree % 2 == 0

def extract_degree_sequence(adjacency_list: Dict[str, List[Tuple[str, float]]]) -> List[int]:
    """
    Extracts degree sequence from a graph.
    Useful for validating the urban map from Week 3.
    """
    degrees = sorted([len(neighbors) for neighbors in adjacency_list.values()], reverse=True)
    return degrees

# Test cases from semana4.html
def main():
    print("=== Validacion de Grafos - Semana 4 (Python) ===\n")
    
    test_cases = [
        ([4, 3, 3, 2, 2, 2, 1, 1], True, "Suma=18 (par), max=4<=7, converge a ceros"),
        ([3, 2, 2, 1], True, "Ejemplo del documento, converge correctamente"),
        ([4, 3, 3, 2, 2, 2], True, "n=6, suma=16 (par), max=4<=5"),
        ([0, 0, 0, 0], True, "Grafo vacio (sin aristas)"),
        ([3, 3, 3, 3], True, "Grafo completo K4 (todos conectados)"),
        ([3, 3, 3, 1], False, "Reduce a [2,2,0] -> [1,-1] (negativo en paso 2)"),
        ([5, 5, 4, 3, 2, 1], False, "Suma=20 (par), pero estructura imposible"),
        ([3, 2, 1], False, "Early exit: max=3 > n-1=2 (falla chequeo inicial)"),
        ([6, 1, 1, 1, 1, 1, 1], False, "n=7, estructura imposible"),
        ([5, 3, 2, 2, 1], False, "Suma=13 (impar) -> imposible en grafo no dirigido")
    ]
    
    print("=== Casos de Prueba Oficiales ===\n")
    passed = 0
    for i, (seq, expected, reason) in enumerate(test_cases, 1):
        result = is_graphical_sequence(seq)
        status = "PASS" if result == expected else "FAIL"
        
        if result == expected:
            passed += 1
        
        print(f"Caso {i}: {seq}")
        print(f"  Esperado: {'Grafica' if expected else 'No Grafica'}")
        print(f"  Resultado: {'Grafica' if result else 'No Grafica'} [{status}]")
        print(f"  Razon: {reason}\n")
    
    print(f"Resultado: {passed}/{len(test_cases)} casos pasados\n")
    
    # Validate city map from Week 3
    print("=== Validacion del Mapa Urbano (Semana 3) ===\n")
    
    # Recreate undirected graph from Week 3
    city_graph = {
        'A': [('B', 2.0), ('C', 3.0)],
        'B': [('A', 2.0), ('D', 1.0)],
        'C': [('A', 3.0), ('E', 4.0)],
        'D': [('B', 1.0), ('F', 5.0)],
        'E': [('C', 4.0), ('F', 2.0)],
        'F': [('D', 5.0), ('E', 2.0)],
        'G': [('H', 6.0)],
        'H': [('G', 6.0)]
    }
    
    extracted_seq = extract_degree_sequence(city_graph)
    is_graphical = is_graphical_sequence(extracted_seq)
    is_consistent = validate_consistency(city_graph)
    
    print(f"Secuencia extraida: {extracted_seq}")
    print(f"Es grafica? {'Si' if is_graphical else 'No'}")
    print(f"Es consistente (suma par)? {'Si' if is_consistent else 'No'}")
    
    print("\n=== Proyecto completado exitosamente! ===")

if __name__ == "__main__":
    main()
