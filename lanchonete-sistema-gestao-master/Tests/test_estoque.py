import unittest
from unittest.mock import patch, MagicMock
from database import estoque

class TestEstoque(unittest.TestCase):

    @patch('database.estoque.conectar')
    def test_visualizar_estoque(self, mock_conectar):
        # Mock da conexão e cursor
        mock_conexao = MagicMock()
        mock_cursor = MagicMock()

        # Configura o retorno da função conectar
        mock_conectar.return_value = mock_conexao
        mock_conexao.cursor.return_value = mock_cursor

        # Simula retorno da consulta com 5 colunas
        mock_cursor.fetchall.return_value = [
            (1, 'X-Burger', 10, 0, '2025-05-16 10:00:00'),
            (2, 'Coca-Cola', 0, 3, '2025-05-15 16:30:00')
        ]

        # Executa a função
        estoque.visualizar_estoque()

        # Verificações
        mock_cursor.execute.assert_called()
        self.assertEqual(mock_cursor.fetchall.call_count, 1)

if __name__ == '__main__':
    unittest.main()

