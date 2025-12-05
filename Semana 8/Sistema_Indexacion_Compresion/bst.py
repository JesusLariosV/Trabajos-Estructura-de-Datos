from typing import List, Optional, Tuple

class NodoBST:
    def __init__(self, valor: str, metadata: Optional[List[Tuple[int, int]]] = None):
        self.valor = valor
        # Metadata: lista de tuplas (linea, columna)
        self.metadata = metadata if metadata is not None else []
        self.izquierdo: Optional['NodoBST'] = None
        self.derecho: Optional['NodoBST'] = None

class BST:
    """
    Árbol Binario de Búsqueda para indexación.
    Almacena palabras y sus posiciones en el texto.
    """
    
    def __init__(self):
        self.raiz = None
    
    def insertar(self, valor: str, pos: Tuple[int, int]):
        """Inserta una palabra y su posición."""
        if not self.raiz:
            self.raiz = NodoBST(valor, [pos])
        else:
            self._insertar_recursivo(self.raiz, valor, pos)
    
    def _insertar_recursivo(self, nodo: NodoBST, valor: str, pos: Tuple[int, int]):
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoBST(valor, [pos])
            else:
                self._insertar_recursivo(nodo.izquierdo, valor, pos)
        elif valor > nodo.valor:
            if nodo.derecho is None:
                nodo.derecho = NodoBST(valor, [pos])
            else:
                self._insertar_recursivo(nodo.derecho, valor, pos)
        else:
            # La palabra ya existe, agregamos la nueva posición
            nodo.metadata.append(pos)
    
    def buscar(self, valor: str) -> List[Tuple[int, int]]:
        """Busca una palabra y retorna sus posiciones."""
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, nodo: NodoBST, valor: str) -> List[Tuple[int, int]]:
        if nodo is None:
            return []
        if valor == nodo.valor:
            return nodo.metadata
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo.derecho, valor)
    
    def eliminar(self, valor: str):
        """Elimina una palabra del índice."""
        self.raiz = self._eliminar_recursivo(self.raiz, valor)
    
    def _eliminar_recursivo(self, nodo: NodoBST, valor: str) -> Optional[NodoBST]:
        if nodo is None:
            return None
        
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)
        else:
            # Caso 1: Hoja
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            
            # Caso 2: Un hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            
            # Caso 3: Dos hijos
            sucesor = self._encontrar_minimo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.metadata = sucesor.metadata # Copiar metadata también
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.valor)
        
        return nodo
    
    def _encontrar_minimo(self, nodo: NodoBST) -> NodoBST:
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual
    
    def inorden(self) -> List[str]:
        """Retorna lista de palabras ordenadas."""
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo: NodoBST, resultado: List[str]):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_recursivo(nodo.derecho, resultado)

    def altura(self) -> int:
        """Calcula la altura del árbol."""
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, nodo: NodoBST) -> int:
        if not nodo:
            return 0
        return 1 + max(self._altura_recursiva(nodo.izquierdo), self._altura_recursiva(nodo.derecho))
