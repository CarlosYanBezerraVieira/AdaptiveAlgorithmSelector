class ArrayRastreado(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trocas = 0
        self.comparacoes = 0

    def __setitem__(self, index, value):
        self.trocas += 1
        super().__setitem__(index, value)

    def resetar_contadores(self):
        self.trocas = 0
        self.comparacoes = 0