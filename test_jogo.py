import unittest
from jogo import Jogo
from jogador import Jogador

class TestJogo(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.jogador1 = Jogador("Edson", "Vermelho")
        self.jogador2 = Jogador("Marcelo", "Azul")
        self.jogador3 = Jogador("Pedro", "Verde")
        self.jogo.adicionar_jogador(self.jogador1)
        self.jogo.adicionar_jogador(self.jogador2)
        self.jogo.adicionar_jogador(self.jogador3)

    def test_receber_objetivo(self):
        self.jogador1.receber_objetivo("Conquistar 3 territórios")
        self.assertEqual(self.jogador1.objetivo, "Conquistar 3 territórios")

    def test_distribuir_territorios(self):
        self.jogo.distribuir_territorios()
        self.assertGreaterEqual(len(self.jogador1.territorios), 1)
        self.assertGreaterEqual(len(self.jogador2.territorios), 1)
        self.assertGreaterEqual(len(self.jogador3.territorios), 1)

    def test_distribuir_exercitos(self):
        self.jogador1.distribuir_exercitos(5)
        self.assertEqual(self.jogador1.exercitos, 5)

    def test_distribuir_cartas(self):
        self.jogo.distribuir_cartas()
        self.assertEqual(len(self.jogador1.cartas), 3)
        self.assertIn(self.jogador1.cartas[0], ["Infantaria", "Cavalaria", "Artilharia"])

    def test_gerar_json(self):
        self.jogo.definir_ordem_jogadores()
        self.jogo.distribuir_territorios()
        self.jogo.distribuir_objetivos()
        self.jogo.iniciar_rodada()
        self.jogo.distribuir_cartas()
        json_data = self.jogo.gerar_json()
        self.assertIn("Edson", json_data)
        self.assertIn("Marcelo", json_data)
        self.assertIn("Pedro", json_data)

if __name__ == '__main__':
    unittest.main()
