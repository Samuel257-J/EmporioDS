import unittest
from unittest.mock import patch
from database.pedido import registrar_pedido, listar_pedidos, editar_pedido, excluir_pedido


class TestPedido(unittest.TestCase):

    @patch('builtins.input', side_effect=['1', '2', '3', 'Pendente', 'Pix'])
    @patch('database.pedido.conectar')
    @patch('database.pedido.atualizar_estoque')
    def test_registrar_pedido(self, mock_atualizar_estoque, mock_conectar, mock_input):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (10.00,)

        registrar_pedido()

        mock_cursor.execute.assert_called()
        mock_conectar.return_value.commit.assert_called()
        mock_atualizar_estoque.assert_called_once_with('2', 3, 'saida')

    @patch('database.pedido.conectar')
    def test_listar_pedidos(self, mock_conectar):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 'João Silva', 'Produto X', 3, 30.00, 'Pendente', 'Cartão')
        ]

        listar_pedidos()

        mock_cursor.execute.assert_called_once()

    @patch('builtins.input', side_effect=['1', '5', 'Entregue', 'Dinheiro'])
    @patch('database.pedido.conectar')
    @patch('database.pedido.atualizar_estoque')
    def test_editar_pedido(self, mock_atualizar_estoque, mock_conectar, mock_input):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        mock_cursor.fetchone.side_effect = [
            (2, 3, 'Pendente', 'Pix'),  # dados do pedido atual
            (10.00,)  # preço do produto
        ]

        editar_pedido()

        self.assertEqual(mock_atualizar_estoque.call_count, 2)
        mock_cursor.execute.assert_called()
        mock_conectar.return_value.commit.assert_called_once()

    @patch('builtins.input', side_effect=['1', 's'])
    @patch('database.pedido.conectar')
    @patch('database.pedido.atualizar_estoque')
    def test_excluir_pedido(self, mock_atualizar_estoque, mock_conectar, mock_input):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (2, 3)

        excluir_pedido()

        mock_atualizar_estoque.assert_called_once_with(2, 3, 'entrada')
        mock_cursor.execute.assert_called()
        mock_conectar.return_value.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()

