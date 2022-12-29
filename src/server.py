from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List,Optional
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

origins = ['http://127.0.0.1:5500']

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

#classe Animal
class Animal(BaseModel):
    id: Optional[str]
    nome: str
    idade: int
    sexo: str
    cor: str

#BANCO FAKE lista tipada da classe Animal
banco: List[Animal] = []

#Metodo get que retorna uma lista de Animal
@app.get("/animais")
def listar_animais():
  return banco

#Metodo get que retorna uma Animal pelo id
@app.get("/animais/{animal_id}")
def obter_animal(animal_id: str):
  for animal in banco: #Busca na lista
      if animal.id == animal_id: # Se encontra o id do parametro retorna o objeto animal
          return animal
  return { "mensagem": f'ID {animal_id} do Animal nao encontrado'} # caso nao encontre o objeto retorna nao encontrado

#INSERE os dados de Animal dentro do BANCO DE DADOS FAKE
@app.post("/animais")
def criar_animal(animal: Animal):
  animal.id = str(uuid4()) # gera id randomicamente UUID e converte para uma String
  banco.append(animal) # Adciona a lista de banco de dados Fake
  return {"mensagem": f'ID {animal.id} do Animal - Criado com Sucesso'}

#DELETA os dados de Animal dentro do BANCO DE DADOS FAKE
@app.delete("/animais/{animal_id}")
def remove_animal(animal_id: str):
  posicao: int = -1
  for index,animal in enumerate(banco): #Busca na lista pelo Indice
      if animal.id == animal_id: # Se encontra o id do parametro retorna o objeto animal
         posicao = index
         break # nao percorre mais o for

  if posicao != -1:
      banco.pop(posicao)
      return { "mensagem": f'ID {animal_id} do Animal removido com sucesso'} # caso encontre o objeto retorna o id deletado
  else:
      return { "mensagem": "Animal nao encontrado"} # caso nao encontre o objeto retorna nao encontrado
