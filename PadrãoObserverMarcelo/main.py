from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List
import random
import json
import os

app = FastAPI()

# Modelos de dados
class Jogador(BaseModel):
    nome: str
    cor: str = None
    objetivo: str = None
    territorios: List[str] = []
    exercitos: int = 0
    cartas: List[str] = []

# Definindo o arquivo JSON
ARQUIVO_JSON = 'dadosOb.json'

# Simulando alguns dados se necessário
cores_disponiveis = ["Vermelho", "Azul", "Verde", "Amarelo"]

jogadores = []

# Carregar dados do arquivo JSON
def carregar_dados():
    global jogadores
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            jogadores = [Jogador(**j) for j in dados['jogadores']]
    else:
        raise HTTPException(status_code=404, detail="Arquivo de dados não encontrado")

# Salvar dados no arquivo JSON
def salvar_dados():
    dados = {
        "jogadores": [j.dict() for j in jogadores]
    }
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

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
    jogador_obj.cor = cor
    cores_disponiveis.remove(cor)
    salvar_dados()
    return {"message": f"O jogador {jogador} escolheu a cor {cor}."}

@app.post("/preparacao/objetivo/")
def receber_objetivo(jogador: str):
    jogador_obj = encontrar_jogador(jogador)
    objetivo = random.choice([
        "Conquistar 3 territórios",
        "Eliminar um jogador",
        "Conquistar 2 continentes",
        "Conquistar 18 territórios",
        "Conquistar 24 territórios",
        "Conquistar a Ásia e a América do Sul",
        "Conquistar a Europa, América do Sul e um terceiro continente",
        "Conquistar a América do Norte e a África"
    ])
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
    territorios_iniciais = [
        "Território 1", "Território 2", "Território 3", 
        "Território 4", "Território 5"
    ]
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

@app.post("/preparacao/distribuir-cartas/")
def distribuir_cartas():
    cartas = ["Infantaria", "Cavalaria", "Artilharia"]
    for jogador in jogadores:
        jogador.cartas = random.sample(cartas, k=3)  # Distribui 3 cartas para cada jogador
    salvar_dados()
    return {j.nome: j.cartas for j in jogadores}

# Rodada
@app.post("/rodada/iniciar/")
def iniciar_rodada():
    for j in jogadores:
        j.exercitos += 5  # 5 exércitos por rodada
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

    # Lógica de combate (simplificada)
    if dados_atacante[0] > dados_defensor[0]:
        defensor.exercitos -= 1  # O defensor perde um exército
        salvar_dados()
        return {"message": f"{jogador_atacante} venceu o ataque no território {territorio_defensor}"}
    else:
        atacante.exercitos -= 1  # O atacante perde um exército
        salvar_dados()
        return {"message": f"{jogador_defensor} defendeu com sucesso o território {territorio_defensor}"}

# Gerar JSON
@app.get("/gerar-json/")
def gerar_json():
    carregar_dados()
    return json.dumps({"jogadores": [j.dict() for j in jogadores]}, indent=4, ensure_ascii=False)
