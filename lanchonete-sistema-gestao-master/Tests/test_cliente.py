import unittest
from unittest.mock import patch
from database.cliente import cadastrar_cliente, listar_clientes, editar_cliente, excluir_cliente

class TestCliente(unittest.TestCase):

    @patch('builtins.input', side_effect=['João Silva', '123.456.789-00', '11999999999', 'Rua A, 123'])
    @patch('database.cliente.conectar')
    def test_cadastrar_cliente(self, mock_conectar, mock_input):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        cadastrar_cliente()
        mock_cursor.execute.assert_called_once()
        mock_conectar.return_value.commit.assert_called_once()

    @patch('database.cliente.conectar')
    def test_listar_clientes(self, mock_conectar):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 'João Silva', '123.456.789-00', '11999999999', 'Rua A, 123')
        ]
        listar_clientes()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM clientes")

    @patch('builtins.input', side_effect=['1', 'Maria Souza', '987.654.321-00', '11888888888', 'Rua B, 456'])
    @patch('database.cliente.conectar')
    def test_editar_cliente(self, mock_conectar, mock_input):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        editar_cliente()
        mock_cursor.execute.assert_called_once()
        mock_conectar.return_value.commit.assert_called_once()

    @patch('builtins.input', side_effect=['1'])
    @patch('database.cliente.conectar')
    def test_excluir_cliente(self, mock_conectar, mock_input):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        excluir_cliente()
        mock_cursor.execute.assert_called_once()
        mock_conectar.return_value.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
