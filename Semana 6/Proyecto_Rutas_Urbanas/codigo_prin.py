from route_optimizer import RouteOptimizer
import json


def main():
    """
    Caso de estudio: Optimización de Rutas Urbanas en una Ciudad
    """
    
    print("=" * 70)
    print("PROYECTO: OPTIMIZACIÓN DE RUTAS URBANAS")
    print("Semana 6 - Algoritmos de Caminos Más Cortos")
    print("=" * 70)
    
    # Crear optimizador
    optimizer = RouteOptimizer()
    
    # Definir red urbana (basada en una ciudad ficticia)
    print("\n[*] Definiendo red urbana...")
    nodes = [
        "Centro Histórico",
        "Zona Industrial",
        "Universidad",
        "Hospital Central",
        "Aeropuerto",
        "Zona Residencial",
        "Parque Central",
        "Estación de Tren"
    ]
    
    # Aristas con distancias en kilómetros
    edges = [
        ("Centro Histórico", "Universidad", 3.5),
        ("Centro Histórico", "Hospital Central", 2.8),
        ("Centro Histórico", "Parque Central", 1.5),
        ("Universidad", "Zona Residencial", 4.2),
        ("Universidad", "Parque Central", 2.0),
        ("Hospital Central", "Aeropuerto", 8.5),
        ("Hospital Central", "Estación de Tren", 3.0),
        ("Aeropuerto", "Zona Industrial", 6.0),
        ("Zona Industrial", "Estación de Tren", 4.5),
        ("Zona Residencial", "Parque Central", 2.5),
        ("Parque Central", "Estación de Tren", 3.2),
        ("Zona Industrial", "Universidad", 5.5)
    ]
    
    optimizer.load_city_network(nodes, edges)
    print(f"[OK] Red cargada: {len(nodes)} nodos, {len(edges)} conexiones")
    
    # ========== PARTE 1: OPTIMIZACIÓN DE RUTAS CON DIJKSTRA ==========
    print("\n" + "=" * 70)
    print("PARTE 1: OPTIMIZACIÓN DE RUTAS (DIJKSTRA)")
    print("=" * 70)
    
    # Rutas de ejemplo
    routes_to_test = [
        ("Centro Histórico", "Aeropuerto"),
        ("Universidad", "Zona Industrial"),
        ("Zona Residencial", "Hospital Central"),
        ("Parque Central", "Aeropuerto"),
        ("Centro Histórico", "Estación de Tren")
    ]
    
    print("\n[RUTAS] Calculando rutas optimas...\n")
    route_results = []
    
    for start, end in routes_to_test:
        path, dist = optimizer.optimize_route(start, end)
        route_results.append({
            'origen': start,
            'destino': end,
            'camino': path,
            'distancia': dist
        })
        
        print(f"Ruta: {start} -> {end}")
        print(f"  Camino optimo: {' -> '.join(path)}")
        print(f"  Distancia: {dist:.2f} km\n")
    
    # ========== PARTE 2: ANÁLISIS DE RED CON FLOYD-WARSHALL ==========
    print("=" * 70)
    print("PARTE 2: ANÁLISIS DE RED (FLOYD-WARSHALL)")
    print("=" * 70)
    
    print("\n[ANALISIS] Analizando red completa...")
    analysis = optimizer.analyze_network()
    
    print("\n[RESULTADOS] Resultados del analisis:")
    print(f"\n  Diámetro de la red: {analysis['diameter']:.2f} km")
    print(f"  (Máxima distancia entre dos puntos cualesquiera)")
    
    print(f"\n  Distancia promedio: {analysis['avg_distance']:.2f} km")
    print(f"  (Promedio de todas las distancias entre pares)")
    
    print("\n  [TOP 3] Nodos mas centrales (menor distancia promedio):")
    for i, (node, avg_dist) in enumerate(analysis['central_nodes'], 1):
        print(f"    {i}. {node}: {avg_dist:.2f} km promedio")
    
    # ========== PARTE 3: SIMULACIÓN DE TRÁFICO ==========
    print("\n" + "=" * 70)
    print("PARTE 3: IMPACTO DEL TRÁFICO")
    print("=" * 70)
    
    # Simular congestión en horas pico
    congested_edges = [
        ("Centro Histórico", "Universidad"),
        ("Centro Histórico", "Hospital Central"),
        ("Universidad", "Zona Residencial")
    ]
    
    print("\n[TRAFICO] Simulando trafico en horas pico...")
    print("   Aristas congestionadas:")
    for edge in congested_edges:
        print(f"     - {edge[0]} <-> {edge[1]}")
    
    impact = optimizer.simulate_traffic_impact(congested_edges, multiplier=2.5)
    
    print(f"\n[RESULTADOS]:")
    print(f"  Distancia promedio SIN tráfico: {impact['baseline_avg']:.2f} km")
    print(f"  Distancia promedio CON tráfico: {impact['traffic_avg']:.2f} km")
    print(f"  Incremento: {impact['increase_pct']:.1f}%")
    
    # Comparar ruta específica con y sin tráfico
    print("\n[COMPARACION] Comparacion de ruta especifica:")
    test_route = ("Centro Histórico", "Aeropuerto")
    
    # Sin tráfico
    path_normal, dist_normal = optimizer.optimize_route(test_route[0], test_route[1])
    
    # Con tráfico
    for edge in congested_edges:
        optimizer.set_traffic(edge, 2.5)
    path_traffic, dist_traffic = optimizer.optimize_route(test_route[0], test_route[1], use_traffic=True)
    
    print(f"\n  Ruta: {test_route[0]} -> {test_route[1]}")
    print(f"\n  SIN trafico:")
    print(f"    Camino: {' -> '.join(path_normal)}")
    print(f"    Distancia: {dist_normal:.2f} km")
    print(f"\n  CON trafico:")
    print(f"    Camino: {' -> '.join(path_traffic)}")
    print(f"    Distancia efectiva: {dist_traffic:.2f} km")
    print(f"    Incremento: {((dist_traffic - dist_normal) / dist_normal * 100):.1f}%")
    
    # ========== PARTE 4: COMPARACIÓN DIJKSTRA VS FLOYD-WARSHALL ==========
    print("\n" + "=" * 70)
    print("PARTE 4: COMPARACIÓN DE ALGORITMOS")
    print("=" * 70)
    
    print("\n[COMPARACION] Dijkstra vs Floyd-Warshall en este grafo:")
    print(f"\n  Tamaño del grafo: {len(nodes)} nodos, {len(edges)} aristas")
    print(f"  Densidad: {len(edges) / (len(nodes) * (len(nodes) - 1) / 2) * 100:.1f}%")
    
    print("\n  Dijkstra:")
    print("    [OK] Ideal para consultas de un origen unico")
    print("    [OK] Complejidad: O((V + E) log V)")
    print("    [OK] Usado en GPS y navegacion en tiempo real")
    
    print("\n  Floyd-Warshall:")
    print("    [OK] Ideal para analisis de red completo")
    print("    [OK] Complejidad: O(V^3)")
    print("    [OK] Usado para precomputar todas las distancias")
    print("    [OK] Detecta ciclos negativos")
    
    print("\n  Recomendacion para este caso:")
    if len(edges) < len(nodes) * (len(nodes) - 1) / 4:
        print("    -> Usar Dijkstra (grafo disperso)")
    else:
        print("    -> Considerar Floyd-Warshall (grafo denso)")
    
    # ========== RESUMEN ==========
    print("\n" + "=" * 70)
    print("RESUMEN DEL PROYECTO")
    print("=" * 70)
    
    print("\n[OK] Implementaciones completadas:")
    print("   • Algoritmo de Dijkstra con heap binario")
    print("   • Algoritmo de Floyd-Warshall con detección de ciclos")
    print("   • Reconstrucción de caminos")
    print("   • Simulación de tráfico dinámico")
    print("   • Análisis de centralidad de nodos")
    
    print("\n[DATOS] Resultados clave:")
    print(f"   • {len(route_results)} rutas óptimas calculadas")
    print(f"   • Nodo más central: {analysis['central_nodes'][0][0]}")
    print(f"   • Impacto del tráfico: +{impact['increase_pct']:.1f}%")
    
    print("\n" + "=" * 70)
    print("Proyecto completado exitosamente [OK]")
    print("=" * 70 + "\n")
    
    # Guardar resultados para el reporte
    results = {
        'routes': route_results,
        'analysis': {
            'diameter': analysis['diameter'],
            'avg_distance': analysis['avg_distance'],
            'central_nodes': analysis['central_nodes']
        },
        'traffic_impact': impact
    }
    
    with open('resultados.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("[GUARDADO] Resultados guardados en 'resultados.json'")


if __name__ == "__main__":
    main()
