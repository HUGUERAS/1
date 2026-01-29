import pytest
from shapely.geometry import Polygon
from unittest.mock import MagicMock
from logic_routes import check_overlap

# Simula uma sessão de banco de dados
class MockDB:
    def execute(self, query, params):
        return self
    
    def fetchall(self):
        # Cenário: Retorna um polígono existente no banco
        # Polígono existente: Quadrado (0 0, 0 2, 2 2, 2 0, 0 0)
        existing_poly = Polygon([(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)])
        return [(existing_poly.wkt,)]

def test_sobreposicao_detectada():
    """
    TESTE DE SOBREPOSIÇÃO (TDD)
    Tenta inserir um polígono que cruza um existente.
    Deve retornar True (tem sobreposição).
    """
    mock_db = MockDB()
    
    # Novo polígono: Quadrado deslocado mas sobreposto (1 1, 1 3, 3 3, 3 1, 1 1)
    # Interseção esperada: Quadrado (1 1, 1 2, 2 2, 2 1, 1 1) -> Área 1.0
    new_poly = Polygon([(1, 1), (1, 3), (3, 3), (3, 1), (1, 1)])
    
    # Executa a lógica
    ha_sobreposicao, msg = check_overlap(new_poly.wkt, mock_db)
    
    # Asserts
    assert ha_sobreposicao is True
    assert "Sobreposição detectada" in msg

def test_vizinho_perfeito_sem_sobreposicao():
    """
    TESTE DE VIZINHANÇA
    Tenta inserir um polígono que toca a borda (vizinho), mas não invade.
    Deve retornar False (não tem sobreposição inválida).
    """
    mock_db = MockDB()
    
    # Novo polígono: Encostado no lado direito (2 0, 2 2, 4 2, 4 0, 2 0)
    # Eles compartilham a aresta x=2. Área de interseção deve ser 0 (apenas linha).
    new_poly = Polygon([(2, 0), (2, 2), (4, 2), (4, 0), (2, 0)])
    
    ha_sobreposicao, msg = check_overlap(new_poly.wkt, mock_db)
    
    assert ha_sobreposicao is False
