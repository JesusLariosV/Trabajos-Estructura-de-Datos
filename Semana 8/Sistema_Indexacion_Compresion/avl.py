from typing import List, Optional, Tuple

class NodoAVL:
    def __init__(self, valor: str, metadata: Optional[List[Tuple[int, int]]] = None):
        self.valor = valor
        self.metadata = metadata if metadata is not None else []
        self.izquierdo: Optional['NodoAVL'] = None
        self.derecho: Optional['NodoAVL'] = None
        self.altura = 1

class AVL:
    """
    Árbol AVL para indexación balanceada.
    """
    
    def __init__(self):
        self.raiz = None
    
    def altura(self, nodo: Optional[NodoAVL]) -> int:
        return nodo.altura if nodo else 0
    
    def factor_balance(self, nodo: Optional[NodoAVL]) -> int:
        if not nodo:
            return 0
        return self.altura(nodo.izquierdo) - self.altura(nodo.derecho)
    
    def actualizar_altura(self, nodo: NodoAVL):
        nodo.altura = 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))
    
    def rotacion_derecha(self, z: NodoAVL) -> NodoAVL:
        y = z.izquierdo
        T3 = y.derecho
        
        y.derecho = z
        z.izquierdo = T3
        
        self.actualizar_altura(z)
        self.actualizar_altura(y)
        
        return y
    
    def rotacion_izquierda(self, z: NodoAVL) -> NodoAVL:
        y = z.derecho
        T2 = y.izquierdo
        
        y.izquierdo = z
        z.derecho = T2
        
        self.actualizar_altura(z)
        self.actualizar_altura(y)
        
        return y
    
    def insertar(self, valor: str, pos: Tuple[int, int]):
        self.raiz = self._insertar_recursivo(self.raiz, valor, pos)
    
    def _insertar_recursivo(self, nodo: Optional[NodoAVL], valor: str, pos: Tuple[int, int]) -> NodoAVL:
        if not nodo:
            return NodoAVL(valor, [pos])
        
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, valor, pos)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, valor, pos)
        else:
            nodo.metadata.append(pos)
            return nodo
        
        self.actualizar_altura(nodo)
        fb = self.factor_balance(nodo)
        
        # Casos de rotación
        # LL
        if fb > 1 and valor < nodo.izquierdo.valor:
            return self.rotacion_derecha(nodo)
        
        # RR
        if fb < -1 and valor > nodo.derecho.valor:
            return self.rotacion_izquierda(nodo)
        
        # LR
        if fb > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        
        # RL
        if fb < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)
        
        return nodo

    def buscar(self, valor: str) -> List[Tuple[int, int]]:
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, nodo: Optional[NodoAVL], valor: str) -> List[Tuple[int, int]]:
        if not nodo:
            return []
        if valor == nodo.valor:
            return nodo.metadata
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo.derecho, valor)

    def inorden(self) -> List[str]:
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo: Optional[NodoAVL], resultado: List[str]):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_recursivo(nodo.derecho, resultado)
