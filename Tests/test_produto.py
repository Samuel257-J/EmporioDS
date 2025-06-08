import unittest
from unittest.mock import patch, MagicMock
from database import produto  # Corrigido o import

class TestProduto(unittest.TestCase):

    @patch('database.produto.input', side_effect=['Pastel de queijo', 'Pastel', '12.00', '10'])
    @patch('database.produto.conectar')
    def test_cadastrar_produto(self, mock_conectar, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        produto.cadastrar_produto()

        mock_cursor.execute.assert_called_once()
        self.assertTrue(mock_conn.commit.called)
        mock_conn.close.assert_called_once()

    @patch('database.produto.conectar')
    def test_listar_produtos(self, mock_conectar):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (2, "Pastel de queijo", "Pastel", 12.00, 10),
            (3, "Pastel de calabresa", "Pastel", 13.00, 8),
            (5, "Pastel de coalho", "Pastel", 14.00, 10),
            (6, "Pastel de frango", "Pastel", 14.00, 8)
        ]
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        with patch('builtins.print') as mock_print:
            produto.listar_produtos()

        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.close.called)
        mock_print.assert_any_call("ID: 2, Nome: Pastel de queijo, Categoria: Pastel, Preço: R$12.00, Estoque: 10")

    @patch('database.produto.input', side_effect=['2', 'Novo Pastel', 'Nova Categoria', '15.00', '12'])
    @patch('database.produto.conectar')
    def test_editar_produto(self, mock_conectar, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        produto.editar_produto()

        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.commit.called)
        self.assertTrue(mock_conn.close.called)

    @patch('database.produto.input', return_value='2')
    @patch('database.produto.conectar')
    def test_excluir_produto(self, mock_conectar, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conectar.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        produto.excluir_produto()

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()

