import unittest
from unittest.mock import patch
from database.funcionario import cadastrar_funcionario, listar_funcionarios, editar_funcionario, excluir_funcionario

class TestFuncionario(unittest.TestCase):

    @patch('builtins.input', side_effect=['Carlos Alberto', 'Gerente', 'carlos', 'senha123'])
    @patch('database.funcionario.conectar')
    def test_cadastrar_funcionario(self, mock_conectar, mock_input):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        cadastrar_funcionario()
        mock_cursor.execute.assert_called_once()
        mock_conectar.return_value.commit.assert_called_once()

    @patch('database.funcionario.conectar')
    def test_listar_funcionarios(self, mock_conectar):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 'Carlos Alberto', 'Gerente', 'carlos', 'senha123')
        ]
        listar_funcionarios()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM funcionarios")

    @patch('builtins.input', side_effect=['1', 'Carlos Alberto', 'Diretor', 'carlosdir', 'novasenha'])
    @patch('database.funcionario.conectar')
    def test_editar_funcionario(self, mock_conectar, mock_input):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        editar_funcionario()
        mock_cursor.execute.assert_called_once()
        mock_conectar.return_value.commit.assert_called_once()

    @patch('builtins.input', side_effect=['1'])
    @patch('database.funcionario.conectar')
    def test_excluir_funcionario(self, mock_conectar, mock_input):
        mock_cursor = mock_conectar.return_value.cursor.return_value
        excluir_funcionario()
        mock_cursor.execute.assert_called_once()
        mock_conectar.return_value.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
