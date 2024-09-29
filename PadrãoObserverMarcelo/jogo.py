# jogo.py
import random
from jogador import Jogador

class Jogo:
    def __init__(self):
        self.jogadores = []
        self.territorios = ["Território 1", "Território 2", "Território 3", "Território 4", "Território 5", "Território 6"]
        self.objetivos = [
            "Conquistar 3 territórios",
            "Eliminar um jogador",
            "Conquistar 2 continentes",
            "Conquistar 18 territórios",
            "Conquistar 24 territórios",
            "Conquistar a Ásia e a América do Sul",
            "Conquistar a Europa, América do Sul e um terceiro continente",
            "Conquistar a América do Norte e a África"
        ]
        self.cartas = ["Infantaria", "Cavalaria", "Artilharia"]
        self.ordem_jogadores = []
        self.observadores = []  # Lista de jogadores observadores

    def adicionar_jogador(self, jogador):
        self.jogadores.append(jogador)
        self.adicionar_observador(jogador)

    # Funções do padrão Observer
    def adicionar_observador(self, jogador):
        self.observadores.append(jogador)

    def remover_observador(self, jogador):
        self.observadores.remove(jogador)

    def notificar_observadores(self, mensagem):
        for observador in self.observadores:
            observador.atualizar(mensagem)

    # Funções do jogo
    def definir_ordem_jogadores(self):
        self.ordem_jogadores = random.sample(self.jogadores, len(self.jogadores))
        self.notificar_observadores("A ordem dos jogadores foi definida.")

    def distribuir_territorios(self):
        random.shuffle(self.territorios)
        for i, jogador in enumerate(self.jogadores):
            jogador.receber_territorios(self.territorios[i::len(self.jogadores)])
        self.notificar_observadores("Os territórios foram distribuídos.")

    def distribuir_objetivos(self):
        for jogador in self.jogadores:
            jogador.receber_objetivo(random.choice(self.objetivos))
        self.notificar_observadores("Os objetivos foram distribuídos.")

    def iniciar_rodada(self):
        for jogador in self.jogadores:
            jogador.distribuir_exercitos(5)
        self.notificar_observadores("Uma nova rodada começou. Exércitos foram distribuídos.")

    def distribuir_cartas(self):
        for jogador in self.jogadores:
            jogador.cartas = random.choices(self.cartas, k=3)
        self.notificar_observadores("Cartas foram distribuídas.")

    def verificar_objetivos_concluidos(self):
        for jogador in self.jogadores:
            if jogador.verificar_objetivo():
                self.notificar_observadores(f"{jogador.nome} conquistou seu objetivo!")
