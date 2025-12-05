from mst import GraphMST
import time

def main():
    print("=" * 70)
    print("PROYECTO: DISEÑO DE RED DE SENSORES DE TRÁFICO")
    print("Semana 7 - Árboles de Expansión Mínima (MST)")
    print("=" * 70)

    # Definición del problema
    # Nodos: Intersecciones principales donde se pueden colocar concentradores
    # Aristas: Posibles conexiones de fibra óptica/cableado con su costo (distancia * dificultad)
    
    nodes = [
        "Centro de Control (0)", 
        "Plaza Norte (1)", 
        "Zona Industrial (2)", 
        "Estadio (3)", 
        "Universidad (4)", 
        "Hospital (5)", 
        "Aeropuerto (6)", 
        "Centro Comercial (7)"
    ]
    
    num_nodes = len(nodes)
    g = GraphMST(num_nodes)
    
    # Conexiones posibles (u, v, costo)
    # Costos en miles de dólares
    connections = [
        (0, 1, 40), (0, 7, 80), # Centro a Norte, Comercial
        (1, 2, 120), (1, 7, 110), # Norte a Industrial, Comercial
        (7, 6, 70), (7, 8, 60), # Comercial a Aeropuerto... espera, nodo 8 no existe, error intencional en datos? no, ajustemos indices
        # Ajustando índices para que coincidan con 0-7
        # 0: Centro, 1: Norte, 2: Ind, 3: Estadio, 4: Univ, 5: Hosp, 6: Aero, 7: Comercial
        
        (0, 1, 40), (0, 7, 80),
        (1, 2, 120), (1, 7, 110),
        (2, 3, 70), (2, 5, 40), (2, 1, 120),
        (3, 2, 70), (3, 4, 90), (3, 5, 140),
        (4, 3, 90), (4, 5, 100),
        (5, 2, 40), (5, 3, 140), (5, 4, 100), (5, 6, 20),
        (6, 5, 20), (6, 7, 10), (6, 8, 60), # Nodo 8?? Asumamos que era un error y es nodo 7 u otro.
        # Vamos a redefinir una red más clara y consistente
    ]
    
    # Redefiniendo conexiones limpias
    # 0: Centro
    # 1: Norte
    # 2: Este
    # 3: Sur
    # 4: Oeste
    # 5: Periferia N
    # 6: Periferia S
    
    nodes = ["Centro", "Norte", "Este", "Sur", "Oeste", "Periferia N", "Periferia S"]
    g = GraphMST(len(nodes))
    
    # (u, v, costo)
    clean_connections = [
        (0, 1, 20), (0, 2, 30), (0, 3, 25), (0, 4, 35), # Centro a cardinales
        (1, 2, 15), (2, 3, 10), (3, 4, 40), (4, 1, 50), # Anillo interior
        (1, 5, 60), (2, 5, 70), # Conexiones a Periferia N
        (3, 6, 55), (4, 6, 45), # Conexiones a Periferia S
        (5, 6, 100) # Conexión lejana entre periferias
    ]
    
    print(f"\n[*] Configurando red de sensores con {len(nodes)} nodos y {len(clean_connections)} posibles conexiones.")
    
    for u, v, w in clean_connections:
        g.add_edge(u, v, w)
        print(f"  - Conexión posible: {nodes[u]} <-> {nodes[v]} [Costo: ${w}k]")

    # --- Ejecución Prim ---
    print("\n" + "-" * 50)
    print("EJECUTANDO ALGORITMO DE PRIM")
    print("-" * 50)
    
    start_time = time.time()
    prim_edges, prim_cost = g.prim_mst(0)
    prim_time = (time.time() - start_time) * 1000
    
    print(f"[OK] MST encontrado con Prim en {prim_time:.4f} ms")
    print(f"Costo Total: ${prim_cost}k")
    print("Conexiones seleccionadas:")
    for u, v, w in prim_edges:
        print(f"  [X] {nodes[u]} <-> {nodes[v]} (${w}k)")

    # --- Ejecución Kruskal ---
    print("\n" + "-" * 50)
    print("EJECUTANDO ALGORITMO DE KRUSKAL")
    print("-" * 50)
    
    start_time = time.time()
    kruskal_edges, kruskal_cost = g.kruskal_mst()
    kruskal_time = (time.time() - start_time) * 1000
    
    print(f"[OK] MST encontrado con Kruskal en {kruskal_time:.4f} ms")
    print(f"Costo Total: ${kruskal_cost}k")
    print("Conexiones seleccionadas:")
    for u, v, w in kruskal_edges:
        print(f"  [X] {nodes[u]} <-> {nodes[v]} (${w}k)")

    # --- Comparación ---
    print("\n" + "=" * 70)
    print("COMPARACIÓN Y ANÁLISIS")
    print("=" * 70)
    
    if prim_cost == kruskal_cost:
        print(f"\n[VERIFICADO] Ambos algoritmos obtuvieron el mismo costo óptimo: ${prim_cost}k")
    else:
        print(f"\n[ERROR] Discrepancia en costos: Prim=${prim_cost}k, Kruskal=${kruskal_cost}k")
        
    print(f"\nAhorro respecto a conectar todo (Costo total posible: ${sum(c[2] for c in clean_connections)}k):")
    total_possible = sum(c[2] for c in clean_connections)
    savings = total_possible - prim_cost
    print(f"  Ahorro: ${savings}k ({savings/total_possible*100:.1f}%)")

    print("\nRecomendación:")
    print("  Para esta red de sensores (grafo denso/disperso intermedio),")
    print("  ambos algoritmos son eficientes. Kruskal es intuitivo para")
    print("  seleccionar las conexiones más baratas primero.")

if __name__ == "__main__":
    main()
