# jogador.py
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
        if self.objetivo:
            continentes_conquistados = set()
            for territorio in self.territorios:
                if "Território" in territorio:  # Supondo que os territórios tenham nomes únicos
                    continente = territorio.split(" ")[0]  # Exemplo: "Território 1" -> "Território"
                    continentes_conquistados.add(continente)
            return all(continente in continentes_conquistados for continente in self.objetivo.split(", "))
        return False

    def atualizar(self, mensagem):
        print(f"{self.nome} foi notificado: {mensagem}")
