
# FIAP - Global Solution 2026
# Modelagem Linear para Aprendizado em Máquina
# Professor: Rodolfo
#
# Henrique de Souza Aragão - RM 570529
# Leonardo Scotti Tobias - RM 573305
# Natan Silva da Costa - RM 573100

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

# 1. Carregar os dados
df = pd.read_csv("data/frota_tratada.csv", sep=";")

colunas = [
    "KM Estimada",
    "Custo Estimado",
    "Passageiros",
    "Custo Analise"
]

dados = df[colunas].dropna()

dados = dados[
    (dados["KM Estimada"] > 0) &
    (dados["Custo Estimado"] > 0)
].copy()

# 2. Criar a classificação
# 0 = Dentro do custo estimado
# 1 = Acima do custo estimado
dados["Acima Estimado"] = (
    dados["Custo Analise"] > dados["Custo Estimado"]
).astype(int)

print("REGRESSÃO LOGÍSTICA BINÁRIA")
print("Quantidade de registros:", len(dados))

print("\nCLASSIFICAÇÃO DAS VIAGENS")
print(dados["Acima Estimado"].value_counts().sort_index())

# 3. Separar as variáveis
x = dados[["KM Estimada", "Custo Estimado", "Passageiros"]]
y = dados["Acima Estimado"]

# Separar treinamento e teste
x_treino, x_teste, y_treino, y_teste = train_test_split(
    x,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# 4. Criar e treinar o modelo
x_treino = sm.add_constant(x_treino)

modelo = sm.Logit(y_treino, x_treino).fit()

print("\nRESULTADOS DO MODELO")
print(modelo.summary())

# 5. Equação da regressão logística
a = modelo.params["const"]
b1 = modelo.params["KM Estimada"]
b2 = modelo.params["Custo Estimado"]
b3 = modelo.params["Passageiros"]

print("\nEQUAÇÃO DA REGRESSÃO LOGÍSTICA")
print(f"Z = {a:.4f} + ({b1:.6f} * KM)")
print(f"    + ({b2:.6f} * Custo Estimado)")
print(f"    + ({b3:.6f} * Passageiros)")
print("P = 1 / (1 + e^(-Z))")

# 6. Previsões dos dados de teste
x_teste = sm.add_constant(x_teste)

probabilidades = modelo.predict(x_teste)
previsoes = (probabilidades >= 0.5).astype(int)

# 7. Matriz de confusão e acurácia
matriz = confusion_matrix(y_teste, previsoes)
acuracia = accuracy_score(y_teste, previsoes)

print("\nAVALIAÇÃO DO MODELO")
print("Matriz de confusão:")
print(matriz)

print(f"\nAcurácia: {acuracia * 100:.2f}%")

# 8. Gráfico da matriz de confusão
plt.figure(figsize=(6, 5))
plt.imshow(matriz, cmap="Blues")

plt.title("Matriz de Confusão - Regressão Logística")
plt.xlabel("Classificação Prevista")
plt.ylabel("Classificação Real")

plt.xticks([0, 1], ["Dentro", "Acima"])
plt.yticks([0, 1], ["Dentro", "Acima"])

for i in range(2):
    for j in range(2):
        plt.text(
            j, i,
            matriz[i, j],
            ha="center",
            va="center"
        )

plt.colorbar()
plt.tight_layout()

plt.savefig("resultados/graficos/matriz_confusao.png")
plt.show()

# 9. Classificar uma nova viagem
nova_viagem = pd.DataFrame({
    "const": [1],
    "KM Estimada": [100],
    "Custo Estimado": [200],
    "Passageiros": [3]
})

probabilidade = modelo.predict(nova_viagem).iloc[0]

print("\nCLASSIFICAÇÃO DE UMA NOVA VIAGEM")
print("Distância estimada: 100 km")
print("Custo estimado: R$ 200,00")
print("Passageiros: 3")

print(f"Probabilidade: {probabilidade * 100:.2f}%")

if probabilidade >= 0.5:
    print("Classificação: Acima do custo estimado")
else:
    print("Classificação: Dentro do custo estimado")

print("\nRegressão logística finalizada!")
