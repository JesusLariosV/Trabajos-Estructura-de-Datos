import heapq
import pickle
from collections import Counter
from typing import Dict, Optional

class NodoHuffman:
    def __init__(self, caracter: Optional[str], frecuencia: int):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierdo: Optional['NodoHuffman'] = None
        self.derecho: Optional['NodoHuffman'] = None
    
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia
    
    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None

class Huffman:
    """
    Clase para compresión y descompresión usando codificación Huffman.
    """
    
    def __init__(self):
        self.raiz = None
        self.codigos: Dict[str, str] = {}
        self.codigos_inversos: Dict[str, str] = {}
    
    def construir_arbol(self, texto: str):
        """Construye el árbol de Huffman a partir de un texto."""
        frecuencias = Counter(texto)
        if not frecuencias:
            return
        
        heap = []
        for char, freq in frecuencias.items():
            heapq.heappush(heap, NodoHuffman(char, freq))
        
        if len(heap) == 1:
            # Caso especial: solo un carácter
            nodo = heapq.heappop(heap)
            self.raiz = NodoHuffman(None, nodo.frecuencia)
            self.raiz.izquierdo = nodo
            self._generar_codigos(self.raiz, "")
            return

        while len(heap) > 1:
            izq = heapq.heappop(heap)
            der = heapq.heappop(heap)
            
            padre = NodoHuffman(None, izq.frecuencia + der.frecuencia)
            padre.izquierdo = izq
            padre.derecho = der
            
            heapq.heappush(heap, padre)
        
        self.raiz = heap[0]
        self._generar_codigos(self.raiz, "")
    
    def _generar_codigos(self, nodo: Optional[NodoHuffman], codigo_actual: str):
        if not nodo:
            return
        
        if nodo.es_hoja():
            # Si es el único nodo en el árbol (caso especial), asignarle '0'
            if not codigo_actual:
                codigo_actual = "0"
            self.codigos[nodo.caracter] = codigo_actual
            self.codigos_inversos[codigo_actual] = nodo.caracter
            return
        
        self._generar_codigos(nodo.izquierdo, codigo_actual + "0")
        self._generar_codigos(nodo.derecho, codigo_actual + "1")
    
    def codificar(self, texto: str) -> str:
        """Retorna la cadena de bits comprimida."""
        if not self.codigos and texto:
            self.construir_arbol(texto)
        return "".join(self.codigos[c] for c in texto)
    
    def decodificar(self, bits: str) -> str:
        """Decodifica una cadena de bits."""
        resultado = []
        nodo_actual = self.raiz
        
        for bit in bits:
            if bit == '0':
                nodo_actual = nodo_actual.izquierdo
            else:
                nodo_actual = nodo_actual.derecho
            
            if nodo_actual.es_hoja():
                resultado.append(nodo_actual.caracter)
                nodo_actual = self.raiz
        
        return "".join(resultado)
    
    def guardar_comprimido(self, filename: str, texto: str):
        """Guarda el texto comprimido y el árbol en un archivo binario."""
        if not self.raiz:
            self.construir_arbol(texto)
        
        bits = self.codificar(texto)
        
        # Padding para completar byte
        padding = 8 - (len(bits) % 8)
        bits += "0" * padding
        
        # Convertir bits a bytes
        b = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            b.append(int(byte, 2))
        
        # Guardar: padding info + árbol (frecuencias) + datos
        # Usamos pickle para serializar las frecuencias, que es suficiente para reconstruir
        frecuencias = Counter(texto)
        
        with open(filename, 'wb') as f:
            pickle.dump(padding, f)
            pickle.dump(frecuencias, f)
            f.write(b)
            
    def cargar_comprimido(self, filename: str) -> str:
        """Carga y descomprime un archivo .huff."""
        with open(filename, 'rb') as f:
            padding = pickle.load(f)
            frecuencias = pickle.load(f)
            bytes_data = f.read()
        
        # Reconstruir árbol
        self.raiz = None
        self.codigos = {}
        heap = []
        for char, freq in frecuencias.items():
            heapq.heappush(heap, NodoHuffman(char, freq))
            
        if len(heap) == 1:
            nodo = heapq.heappop(heap)
            self.raiz = NodoHuffman(None, nodo.frecuencia)
            self.raiz.izquierdo = nodo
        else:
            while len(heap) > 1:
                izq = heapq.heappop(heap)
                der = heapq.heappop(heap)
                padre = NodoHuffman(None, izq.frecuencia + der.frecuencia)
                padre.izquierdo = izq
                padre.derecho = der
                heapq.heappush(heap, padre)
            self.raiz = heap[0]
            
        self._generar_codigos(self.raiz, "")
        
        # Convertir bytes a bits
        bits = ""
        for byte in bytes_data:
            bits += f"{byte:08b}"
        
        # Quitar padding
        if padding > 0:
            bits = bits[:-padding]
            
        return self.decodificar(bits)
