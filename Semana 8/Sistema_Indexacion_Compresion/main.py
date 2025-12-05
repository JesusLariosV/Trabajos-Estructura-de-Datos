import os
import time
from bst import BST
from avl import AVL
from huffman import Huffman

def cargar_texto(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] El archivo '{filename}' no existe.")
        return None
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def limpiar_palabra(palabra):
    return "".join(c for c in palabra if c.isalnum()).lower()

def construir_indice(texto, estructura_tipo="AVL"):
    if estructura_tipo == "BST":
        indice = BST()
    else:
        indice = AVL()
    
    lines = texto.splitlines()
    count = 0
    start_time = time.time()
    
    for i, line in enumerate(lines):
        words = line.split()
        for j, word in enumerate(words):
            clean = limpiar_palabra(word)
            if clean:
                indice.insertar(clean, (i + 1, j + 1))
                count += 1
                
    end_time = time.time()
    return indice, count, (end_time - start_time) * 1000

def main():
    print("=" * 70)
    print("SISTEMA DE INDEXACIÓN Y COMPRESIÓN (Semana 8)")
    print("=" * 70)
    
    filename = "sample_text.txt"
    
    # Generar archivo de muestra si no existe
    if not os.path.exists(filename):
        print(f"[*] Generando archivo de prueba '{filename}'...")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("""
El ingenioso hidalgo don Quijote de la Mancha
En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor. Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos los sábados, lantejas los viernes, algún palomino de añadidura los domingos, consumían las tres partes de su hacienda. El resto della concluían sayo de velarte, calzas de velludo para las fiestas, con sus pantuflos de lo mismo, y los días de entresemana se honraba con su vellorí de lo más fino. Tenía en su casa una ama que pasaba de los cuarenta, y una sobrina que no llegaba a los veinte, y un mozo de campo y plaza, que así ensillaba el rocín como tomaba la podadera. Frisaba la edad de nuestro hidalgo con los cincuenta años; era de complexión recia, seco de carnes, enjuto de rostro, gran madrugador y amigo de la caza. Quieren decir que tenía el sobrenombre de Quijada, o Quesada, que en esto hay alguna diferencia en los autores que deste caso escriben; aunque por conjeturas verosímiles se deja entender que se llamaba Quijana. Pero esto importa poco a nuestro cuento: basta que en la narración dél no se salga un punto de la verdad.
            """.strip())
    
    texto = cargar_texto(filename)
    if not texto:
        return

    while True:
        print("\nMENÚ PRINCIPAL:")
        print("1. Construir Índice (BST vs AVL)")
        print("2. Buscar Palabra")
        print("3. Comprimir Archivo (Huffman)")
        print("4. Ver Estadísticas")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            print("\n--- Construcción de Índice ---")
            print("Comparando tiempos de construcción...")
            
            # BST
            bst, count, time_bst = construir_indice(texto, "BST")
            print(f"BST: {count} palabras indexadas en {time_bst:.4f} ms. Altura: {bst.altura()}")
            
            # AVL
            avl, count, time_avl = construir_indice(texto, "AVL")
            print(f"AVL: {count} palabras indexadas en {time_avl:.4f} ms. Altura: {avl.altura(avl.raiz)}")
            
            # Guardar el AVL para búsquedas (es más eficiente)
            indice_actual = avl
            print("[OK] Índice AVL seleccionado para búsquedas.")
            
        elif opcion == "2":
            if 'indice_actual' not in locals():
                print("[!] Primero construya el índice (Opción 1).")
                continue
            
            palabra = input("Ingrese palabra a buscar: ").lower()
            resultados = indice_actual.buscar(palabra)
            
            if resultados:
                print(f"\n[ENCONTRADO] '{palabra}' aparece {len(resultados)} veces:")
                for linea, col in resultados:
                    print(f"  - Línea {linea}, Columna {col}")
            else:
                print(f"\n[NO ENCONTRADO] La palabra '{palabra}' no está en el índice.")
                
        elif opcion == "3":
            print("\n--- Compresión Huffman ---")
            huff = Huffman()
            output_file = filename.replace(".txt", ".huff")
            
            start = time.time()
            huff.guardar_comprimido(output_file, texto)
            end = time.time()
            
            orig_size = os.path.getsize(filename)
            comp_size = os.path.getsize(output_file)
            
            print(f"[OK] Archivo comprimido guardado en '{output_file}'")
            print(f"Tiempo: {(end-start)*1000:.4f} ms")
            print(f"Original: {orig_size} bytes")
            print(f"Comprimido: {comp_size} bytes")
            print(f"Reducción: {100 - (comp_size/orig_size*100):.2f}%")
            
            # Verificar integridad
            texto_recup = huff.cargar_comprimido(output_file)
            if texto == texto_recup:
                print("[VERIFICADO] La descompresión coincide con el original.")
            else:
                print("[ERROR] La descompresión falló.")
                
        elif opcion == "4":
            if 'indice_actual' not in locals():
                print("[!] Primero construya el índice.")
                continue
            print("\n--- Estadísticas ---")
            print(f"Total palabras: {count}")
            print(f"Altura del árbol (AVL): {indice_actual.altura(indice_actual.raiz)}")
            print(f"Factor de balance raíz: {indice_actual.factor_balance(indice_actual.raiz)}")
            
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    # Pequeño fix para importar clases si se ejecuta directamente
    # (Asumiendo que están en el mismo directorio)
    try:
        from bst import BST
        from avl import AVL
        from huffman import Huffman
        main()
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrate de estar en el directorio correcto.")
