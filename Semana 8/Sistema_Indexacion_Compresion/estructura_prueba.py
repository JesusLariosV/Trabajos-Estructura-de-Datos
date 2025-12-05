import pytest
from bst import BST
from avl import AVL
from huffman import Huffman
import os

# --- Tests BST ---
def test_bst_insert_search():
    bst = BST()
    bst.insertar("hola", (1, 1))
    bst.insertar("mundo", (1, 2))
    bst.insertar("hola", (2, 1)) # Duplicado (nueva posición)
    
    assert bst.buscar("hola") == [(1, 1), (2, 1)]
    assert bst.buscar("mundo") == [(1, 2)]
    assert bst.buscar("inexistente") == []

def test_bst_delete():
    bst = BST()
    bst.insertar("a", (1,1))
    bst.insertar("b", (1,2))
    bst.insertar("c", (1,3))
    
    bst.eliminar("b")
    assert bst.buscar("b") == []
    assert bst.inorden() == ["a", "c"]

def test_bst_height():
    bst = BST()
    for i in range(5):
        bst.insertar(str(i), (1,1))
    # 0 -> 1 -> 2 -> 3 -> 4 (degenerado)
    assert bst.altura() == 5

# --- Tests AVL ---
def test_avl_balance():
    avl = AVL()
    # Insertar en orden que causaría degeneración en BST
    # 1, 2, 3 -> Rotación izquierda
    avl.insertar("1", (1,1))
    avl.insertar("2", (1,1))
    avl.insertar("3", (1,1))
    
    assert avl.altura(avl.raiz) == 2 # Balanceado
    assert avl.raiz.valor == "2" # Nueva raíz

def test_avl_rotations():
    avl = AVL()
    # Caso LR: 30, 10, 20
    avl.insertar("30", (1,1))
    avl.insertar("10", (1,1))
    avl.insertar("20", (1,1))
    
    assert avl.altura(avl.raiz) == 2
    assert avl.raiz.valor == "20"

# --- Tests Huffman ---
def test_huffman_coding():
    h = Huffman()
    texto = "ABRACADABRA"
    h.construir_arbol(texto)
    
    codificado = h.codificar(texto)
    decodificado = h.decodificar(codificado)
    
    assert texto == decodificado
    assert len(codificado) < len(texto) * 8 # Debe comprimir

def test_huffman_file_io(tmp_path):
    h = Huffman()
    texto = "Este es un texto de prueba para compresión."
    archivo = tmp_path / "test.huff"
    
    h.guardar_comprimido(str(archivo), texto)
    
    h2 = Huffman()
    texto_recuperado = h2.cargar_comprimido(str(archivo))
    
    assert texto == texto_recuperado

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
