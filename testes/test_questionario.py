import unittest
from unittest.mock import patch
from analisador.questionario import executar_questionario

class TestQuestionario(unittest.TestCase):

    @patch('builtins.input', side_effect=['1', '2', '2', 'N', 'N', 'N', '1', '1'])
    def test_ordenacao_padrao_simples(self, mock_input):
        """
        Teste 1: Ordenar, Tamanho Médio, Aleatório, Sem duplicatas,
        Sem estabilidade, Sem restrição de memória, Tipo simples, Cabe na RAM.
        Respostas: 
        1. Ordenar -> '1'
        2. Médio -> '2'
        3. Aleatório -> '2'
        4. Duplicatas -> 'N'
        5. Estabilidade -> 'N'
        6. Memória -> 'N'
        7. Tipo -> '1'
        8. Disco -> '1'
        """
        props = executar_questionario()
        self.assertEqual(props["objetivo"], "ordenar")
        self.assertEqual(props["tamanho"], 5000)
        self.assertEqual(props["grau_ordenacao"], 0.5)
        self.assertEqual(props["percentual_duplicatas"], 0.0)
        self.assertFalse(props["precisa_estabilidade"])
        self.assertFalse(props["restricao_memoria"])
        self.assertEqual(props["tipo_dados"], "int")
        self.assertFalse(props["dados_em_disco"])
        self.assertEqual(props["origem"], "Declarada")

    @patch('builtins.input', side_effect=['2', '1', '1', 'S', 'S', '2', '2'])
    def test_busca_repetitiva_ordenada(self, mock_input):
        """
        Teste 2: Buscar, Tamanho Pequeno, Já Ordenado, Muitas duplicatas,
        Restrição severa de memória, Objetos complexos, Busca milhares de vezes.
        Respostas:
        1. Buscar -> '2'
        2. Pequeno -> '1'
        3. Já ordenado -> '1'
        4. Duplicatas -> 'S'
        6. Memória -> 'S' (pula estabilidade pq é busca)
        7. Tipo -> '2' (complexo)
        8. Busca milhares de vezes -> '2'
        """
        props = executar_questionario()
        self.assertEqual(props["objetivo"], "buscar")
        self.assertEqual(props["tamanho"], 50)
        self.assertEqual(props["grau_ordenacao"], 0.0)
        self.assertEqual(props["percentual_duplicatas"], 50.0)
        self.assertTrue(props["restricao_memoria"])
        self.assertEqual(props["tipo_dados"], "object")
        self.assertTrue(props["busca_frequente"])

    @patch('builtins.input', side_effect=['1', '3', '3', 'N', 'S', 'N', '2', '2'])
    def test_ordenacao_externa_complexa(self, mock_input):
        """
        Teste 3: Ordenar, Tamanho Grande, Invertidos, Sem duplicatas,
        Exige estabilidade, Sem restrição de memória (virtual), Tipo complexo, Em Disco.
        Respostas:
        1. Ordenar -> '1'
        2. Grande -> '3'
        3. Invertidos -> '3'
        4. Duplicatas -> 'N'
        5. Estabilidade -> 'S'
        6. Memória -> 'N'
        7. Tipo complexo -> '2'
        8. Paginação/Disco -> '2'
        """
        props = executar_questionario()
        self.assertEqual(props["objetivo"], "ordenar")
        self.assertEqual(props["tamanho"], 100000)
        self.assertEqual(props["grau_ordenacao"], 1.0)
        self.assertEqual(props["percentual_duplicatas"], 0.0)
        self.assertTrue(props["precisa_estabilidade"])
        self.assertFalse(props["restricao_memoria"])
        self.assertEqual(props["tipo_dados"], "object")
        self.assertTrue(props["dados_em_disco"])
        
    @patch('builtins.input', side_effect=['1', '1', '1', 'S', 'N', 'S', '1', '1'])
    def test_ordenacao_quase_ordenado_pequeno(self, mock_input):
        """
        Teste 4: Ordenar, Pequeno, Quase ordenado, Com duplicatas.
        Respostas: 1, 1, 1, S, N, S, 1, 1
        """
        props = executar_questionario()
        self.assertEqual(props["objetivo"], "ordenar")
        self.assertEqual(props["tamanho"], 50)
        self.assertEqual(props["grau_ordenacao"], 0.05)
        self.assertEqual(props["percentual_duplicatas"], 50.0)
        self.assertTrue(props["restricao_memoria"])

if __name__ == '__main__':
    unittest.main()
