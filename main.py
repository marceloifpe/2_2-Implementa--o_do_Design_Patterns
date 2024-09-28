from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random
import json
import os

app = FastAPI()

# Modelos de dados
class Jogador(BaseModel):
    nome: str
    cor_exercito: str = None
    objetivo: str = None
    territorios: List[str] = []
    exercitos: int = 0
    cartas: List[str] = []

# Simulando alguns dados
territorios_iniciais = ["Território 1", "Território 2", "Território 3", "Território 4", "Território 5"]
objetivos_possiveis = ["Conquistar 24 territórios", "Eliminar um oponente", "Controlar dois continentes"]
cores_disponiveis = ["Vermelho", "Azul", "Verde", "Amarelo"]
cartas_possiveis = ["Carta 1", "Carta 2", "Carta 3"]

jogadores = []

# Carregar dados do arquivo JSON
def carregar_dados():
    global jogadores
    if os.path.exists('dados.json'):
        with open('dados.json', 'r') as f:
            dados = json.load(f)
            jogadores = [Jogador(**j) for j in dados['jogadores']]

# Salvar dados no arquivo JSON
def salvar_dados():
    dados = {
        "jogadores": [j.dict() for j in jogadores]
    }
    with open('dados.json', 'w') as f:
        json.dump(dados, f, indent=4)

# Encontrar jogador
def encontrar_jogador(nome: str) -> Jogador:
    for j in jogadores:
        if j.nome == nome:
            return j
    raise HTTPException(status_code=404, detail="Jogador não encontrado")

# Função auxiliar para rolar dados
def rolar_dados(quantidade: int) -> List[int]:
    return sorted([random.randint(1, 6) for _ in range(quantidade)], reverse=True)

@app.on_event("startup")
async def startup_event():
    carregar_dados()

# Preparação
@app.post("/jogadores/adicionar/")
def adicionar_jogador(nome: str):
    if any(j.nome == nome for j in jogadores):
        raise HTTPException(status_code=400, detail="Jogador já existe")
    jogador = Jogador(nome=nome)
    jogadores.append(jogador)
    salvar_dados()
    return {"message": f"Jogador {jogador.nome} adicionado com sucesso"}

@app.post("/preparacao/escolher-cor/")
def escolher_cor(jogador: str, cor: str):
    if cor not in cores_disponiveis:
        return {"error": "Cor não disponível"}
    jogador_obj = encontrar_jogador(jogador)
    jogador_obj.cor_exercito = cor
    cores_disponiveis.remove(cor)
    salvar_dados()
    return {"message": f"O jogador {jogador} escolheu a cor {cor}."}

@app.post("/preparacao/objetivo/")
def receber_objetivo(jogador: str):
    jogador_obj = encontrar_jogador(jogador)
    objetivo = random.choice(objetivos_possiveis)
    jogador_obj.objetivo = objetivo
    salvar_dados()
    return {"message": f"Objetivo do jogador {jogador}: {objetivo}"}

@app.post("/preparacao/definir-ordem/")
def definir_ordem():
    random.shuffle(jogadores)
    ordem = [j.nome for j in jogadores]
    salvar_dados()
    return {"ordem": ordem}

@app.post("/preparacao/distribuir-territorios/")
def distribuir_territorios():
    random.shuffle(territorios_iniciais)
    for i, jogador in enumerate(jogadores):
        jogador.territorios.append(territorios_iniciais[i % len(jogadores)])
    salvar_dados()
    return {j.nome: j.territorios for j in jogadores}

@app.post("/preparacao/distribuir-exercitos/")
def distribuir_exercitos(jogador: str, exercitos: int):
    jogador_obj = encontrar_jogador(jogador)
    jogador_obj.exercitos += exercitos
    salvar_dados()
    return {"message": f"{exercitos} exércitos distribuídos para o jogador {jogador}"}

# Rodada
@app.post("/rodada/iniciar/")
def iniciar_rodada():
    for j in jogadores:
        j.exercitos += 5  #  5 exércitos por rodada
    salvar_dados()
    return {j.nome: j.exercitos for j in jogadores}

@app.post("/rodada/ataque/")
def iniciar_ataque(jogador_atacante: str, territorio_atacante: str, jogador_defensor: str, territorio_defensor: str):
    atacante = encontrar_jogador(jogador_atacante)
    defensor = encontrar_jogador(jogador_defensor)
    
    if territorio_atacante not in atacante.territorios or territorio_defensor not in defensor.territorios:
        return {"error": "Territórios inválidos para ataque"}
    
    # Rolar dados para atacante e defensor
    dados_atacante = rolar_dados(min(3, atacante.exercitos - 1))  # Ataque com até 3 exércitos
    dados_defensor = rolar_dados(min(2, defensor.exercitos))      # Defesa com até 2 exércitos
    
    perdas_atacante = 0
    perdas_defensor = 0
    
    # Verifica os dados para determinar perdas
    for dado_atacante, dado_defensor in zip(dados_atacante, dados_defensor):
        if dado_atacante > dado_defensor:
            perdas_defensor += 1
        else:
            perdas_atacante += 1
    
    atacante.exercitos -= perdas_atacante
    defensor.exercitos -= perdas_defensor
    
    # Se o defensor perde todos os exércitos, atacante conquista o território
    if defensor.exercitos <= 0:
        defensor.territorios.remove(territorio_defensor)
        atacante.territorios.append(territorio_defensor)
    
    salvar_dados()
    return {
        "resultados_dados": {
            "atacante": dados_atacante,
            "defensor": dados_defensor
        },
        "resultado_batalha": {
            "atacante": {"nome": atacante.nome, "perdas": perdas_atacante, "exercitos_restantes": atacante.exercitos},
            "defensor": {"nome": defensor.nome, "perdas": perdas_defensor, "exercitos_restantes": defensor.exercitos},
        },
        "conquista": f"{atacante.nome} conquistou {territorio_defensor}" if defensor.exercitos <= 0 else "Território não conquistado"
    }

@app.post("/rodada/receber-cartas/")
def receber_cartas(jogador: str):
    jogador_obj = encontrar_jogador(jogador)
    carta = random.choice(cartas_possiveis)
    jogador_obj.cartas.append(carta)
    salvar_dados()
    return {"message": f"O jogador {jogador} recebeu a carta {carta}"}

@app.post("/rodada/mover-exercitos/")
def mover_exercitos(jogador: str, origem: str, destino: str, quantidade: int):
    jogador_obj = encontrar_jogador(jogador)
    if origem not in jogador_obj.territorios or destino not in jogador_obj.territorios:
        return {"error": "Movimento inválido entre territórios não controlados"}
    
    # Lógica simples para mover exércitos entre territórios do mesmo jogador
    salvar_dados()
    return {"message": f"{jogador} moveu {quantidade} exércitos de {origem} para {destino}"}

@app.post("/rodada/troca-cartas/")
def trocar_cartas(jogador: str, cartas: List[str]):
    jogador_obj = encontrar_jogador(jogador)
    # Adicione lógica para troca de cartas (regras do jogo War)
    salvar_dados()
    return {"message": f"{jogador} trocou as cartas {cartas}"}

@app.get("/objetivo/verificar/")
def verificar_objetivo(jogador: str):
    jogador_obj = encontrar_jogador(jogador)
    # Verificação fictícia, adicionar lógica para verificar condição de vitória
    return {"message": f"O jogador {jogador} não completou o objetivo ainda"}

# Nova rota para visualizar informações de um jogador
@app.get("/jogadores/ver/")
def ver_jogador(nome: str):
    jogador = encontrar_jogador(nome)
    return {
        "nome": jogador.nome,
        "cor_exercito": jogador.cor_exercito,
        "objetivo": jogador.objetivo,
        "territorios": jogador.territorios,
        "exercitos": jogador.exercitos,
        "cartas": jogador.cartas
    }
