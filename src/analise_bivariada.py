
# FIAP - Global Solution 2026
# Modelagem Linear para Aprendizado em Máquina
# Professor: Rodolfo
#
# Henrique de Souza Aragão - RM 570529
# Leonardo Scotti Tobias - RM 573305
# Natan Silva da Costa - RM 573100

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress, f

# 1. Carregar a base tratada
df = pd.read_csv("data/frota_tratada.csv", sep=";")

# Selecionar as duas variáveis
dados = df[["KM Real", "Custo Analise"]].dropna()

# Considerar apenas viagens com distância positiva
dados = dados[dados["KM Real"] > 0]

x = dados["KM Real"]
y = dados["Custo Analise"]

print("ANÁLISE BIVARIADA")
print("Quantidade de registros:", len(dados))

# 2. Gráfico de dispersão
plt.figure(figsize=(9, 5))
plt.scatter(x, y, alpha=0.3)

plt.title("Distância percorrida x Custo da viagem")
plt.xlabel("KM Real")
plt.ylabel("Custo Real (R$)")
plt.grid(True)

plt.savefig("resultados/graficos/dispersao.png")
plt.show()

# 3. Covariância e correlação de Pearson
covariancia = x.cov(y)
correlacao = x.corr(y)

print("\nCOVARIÂNCIA E CORRELAÇÃO")
print(f"Covariância: {covariancia:.2f}")
print(f"Correlação de Pearson: {correlacao:.4f}")

if correlacao > 0:
    print("Correlação positiva")
elif correlacao < 0:
    print("Correlação negativa")
else:
    print("Correlação nula")

# 4. Gráfico de correlação de Pearson
matriz = dados.corr()

plt.figure(figsize=(6, 5))
plt.imshow(matriz, cmap="coolwarm", vmin=-1, vmax=1)

plt.xticks([0, 1], matriz.columns)
plt.yticks([0, 1], matriz.columns)

for i in range(2):
    for j in range(2):
        plt.text(
            j, i,
            f"{matriz.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.colorbar(label="Correlação")
plt.title("Correlação de Pearson")

plt.tight_layout()
plt.savefig("resultados/graficos/correlacao_bivariada.png")
plt.show()

# 5. Regressão linear simples
regressao = linregress(x, y)

a = regressao.intercept
b = regressao.slope

print("\nREGRESSÃO LINEAR SIMPLES")
print(f"Equação: Y = {a:.2f} + {b:.4f} * X")

# Gráfico de dispersão com reta
plt.figure(figsize=(9, 5))

plt.scatter(x, y, alpha=0.3, label="Dados reais")

valores_x = np.linspace(x.min(), x.max(), 100)
valores_y = a + b * valores_x

plt.plot(
    valores_x,
    valores_y,
    color="red",
    label="Regressão Linear"
)

plt.title("Regressão Linear - KM x Custo")
plt.xlabel("KM Real")
plt.ylabel("Custo Real (R$)")
plt.legend()
plt.grid(True)

plt.savefig("resultados/graficos/regressao_simples.png")
plt.show()

# 6. Verificação do modelo
r2 = regressao.rvalue ** 2

n = len(dados)
f_calculado = (r2 / (1 - r2)) * (n - 2)
valor_p_f = f.sf(f_calculado, 1, n - 2)

print("\nAVALIAÇÃO DO MODELO")
print(f"R²: {r2:.4f}")
print(f"R² em porcentagem: {r2 * 100:.2f}%")
print(f"Teste F: {f_calculado:.4f}")
print(f"Valor-p do Teste F: {valor_p_f:.6f}")

if valor_p_f < 0.05:
    print("Regressão estatisticamente significativa")
else:
    print("Regressão não significativa")

# 7. Previsão
km_previsto = 100
custo_previsto = a + b * km_previsto

print("\nPREVISÃO")
print(f"Distância: {km_previsto} km")
print(f"Custo previsto: R$ {custo_previsto:.2f}")

print("\nAnálise bivariada finalizada!")
