from utils.contador import ContadorInstrumentacao

class TabelaHashInstrumentada:
    """
    Simulação de Busca baseada em Hash O(1) usando o dicionário 
    nativo do Python integrado com o nosso Contador.
    """
    def __init__(self, arr):
        # O processo de construção (inserção)
        self.tabela = {elemento: idx for idx, elemento in enumerate(arr)}
        
    def buscar(self, alvo, contador: ContadorInstrumentacao):
        contador.registrar_comparacao() # Verifica se a chave existe na estrutura hash
        if alvo in self.tabela:
            return self.tabela[alvo]
        return -1