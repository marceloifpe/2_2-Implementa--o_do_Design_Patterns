class Jogador:
    def __init__(self, nome, cor):
        self.nome = nome
        self.cor = cor
        self.objetivo = None
        self.territorios = []
        self.exercitos = 0
        self.cartas = []

    def receber_objetivo(self, objetivo):
        self.objetivo = objetivo

    def receber_territorios(self, territorios):
        self.territorios = territorios

    def distribuir_exercitos(self, exercitos):
        self.exercitos += exercitos

    def mover_exercitos(self, origem, destino, quantidade):
        if origem in self.territorios and destino in self.territorios and self.exercitos >= quantidade:
            self.exercitos -= quantidade
            

    def verificar_objetivo(self):
       
        pass
