class ContadorInstrumentacao:
    def __init__(self):
        self.comparacoes = 0
        self.trocas = 0

    def registrar_comparacao(self):
        self.comparacoes += 1

    def registrar_troca(self):
        self.trocas += 1

    def resetar(self):
        self.comparacoes = 0
        self.trocas = 0

    def obter_resultados(self):
        return {
            "comparacoes": self.comparacoes,
            "trocas": self.trocas
        }