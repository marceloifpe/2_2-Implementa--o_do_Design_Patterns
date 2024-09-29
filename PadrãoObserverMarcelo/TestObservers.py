import unittest
import logging
from jogo import Jogo
from jogador import Jogador

# Configurando o logger para capturar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestObserver(unittest.TestCase):
    def setUp(self):
        self.jogo = Jogo()
        self.jogador1 = Jogador("Edson", "Vermelho")
        self.jogador2 = Jogador("Marcelo", "Azul")
        self.jogo.adicionar_jogador(self.jogador1)
        self.jogo.adicionar_jogador(self.jogador2)

    def test_notificar_observadores(self):
        # Capturando os logs durante o teste
        with self.assertLogs(logger, level='INFO') as log:
            self.jogo.iniciar_rodada()
            # Verificando se os logs de notificação estão presentes
            self.assertIn("INFO:__main__:Edson foi notificado", log.output)
            self.assertIn("INFO:__main__:Marcelo foi notificado", log.output)

if __name__ == '__main__':
    unittest.main()
