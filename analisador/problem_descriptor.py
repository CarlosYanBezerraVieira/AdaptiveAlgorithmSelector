from dataclasses import dataclass

@dataclass
class DescritorProblema:
    """
    Classe que armazena os requisitos não-funcionais do problema do usuário.
    """
    exige_estabilidade: bool = False
    restricao_memoria: bool = False
    prioriza_tempo_execucao: bool = True
    
    def atualizar_requisito(self, parametro: str, valor: bool):
        if hasattr(self, parametro):
            setattr(self, parametro, valor)