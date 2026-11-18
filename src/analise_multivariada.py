
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

# 1. Carregar os dados
df = pd.read_csv("data/frota_tratada.csv", sep=";")

colunas = ["KM Real", "Passageiros", "Custo Analise"]

dados = df[colunas].dropna()
dados = dados[dados["KM Real"] > 0]

print("ANÁLISE MULTIVARIADA")
print("Quantidade de registros:", len(dados))

# 2. Gráficos de dispersão
fig, graficos = plt.subplots(1, 3, figsize=(15, 4))

graficos[0].scatter(dados["KM Real"], dados["Custo Analise"], alpha=0.3)
graficos[0].set_xlabel("KM Real")
graficos[0].set_ylabel("Custo (R$)")
graficos[0].set_title("KM x Custo")

graficos[1].scatter(dados["Passageiros"], dados["Custo Analise"], alpha=0.3)
graficos[1].set_xlabel("Passageiros")
graficos[1].set_ylabel("Custo (R$)")
graficos[1].set_title("Passageiros x Custo")

graficos[2].scatter(dados["KM Real"], dados["Passageiros"], alpha=0.3)
graficos[2].set_xlabel("KM Real")
graficos[2].set_ylabel("Passageiros")
graficos[2].set_title("KM x Passageiros")

plt.tight_layout()
plt.savefig("resultados/graficos/dispersao_multivariada.png")
plt.show()

# 3. Matrizes de covariância e correlação
covariancia = dados.cov()
correlacao = dados.corr()

print("\nMATRIZ DE COVARIÂNCIA")
print(covariancia.round(2))

print("\nMATRIZ DE CORRELAÇÃO DE PEARSON")
print(correlacao.round(4))

# 4. Gráfico de correlação
plt.figure(figsize=(7, 5))
plt.imshow(correlacao, cmap="coolwarm", vmin=-1, vmax=1)

plt.xticks(range(3), colunas, rotation=20)
plt.yticks(range(3), colunas)

for i in range(3):
    for j in range(3):
        plt.text(
            j, i,
            f"{correlacao.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.colorbar(label="Correlação")
plt.title("Correlação de Pearson - Multivariada")
plt.tight_layout()

plt.savefig("resultados/graficos/correlacao_multivariada.png")
plt.show()

# 5. Regressão linear múltipla
x = dados[["KM Real", "Passageiros"]]
y = dados["Custo Analise"]

x = sm.add_constant(x)

modelo = sm.OLS(y, x).fit()

print("\nREGRESSÃO LINEAR MÚLTIPLA")
print(modelo.summary())

a = modelo.params["const"]
b1 = modelo.params["KM Real"]
b2 = modelo.params["Passageiros"]

print("\nEQUAÇÃO DA REGRESSÃO")
print(f"Y = {a:.2f} + {b1:.4f} * KM + {b2:.4f} * Passageiros")

# 6. Avaliação do modelo
print("\nAVALIAÇÃO DO MODELO")
print(f"R²: {modelo.rsquared:.4f}")
print(f"R² ajustado: {modelo.rsquared_adj:.4f}")
print(f"Teste F: {modelo.fvalue:.4f}")
print(f"Valor-p: {modelo.f_pvalue:.6f}")

if modelo.f_pvalue < 0.05:
    print("Regressão estatisticamente significativa")
else:
    print("Regressão não significativa")

# 7. Previsão
km = 100
passageiros = 3

previsao = a + b1 * km + b2 * passageiros

print("\nPREVISÃO")
print(f"Distância: {km} km")
print(f"Passageiros: {passageiros}")
print(f"Custo previsto: R$ {previsao:.2f}")

print("\nAnálise multivariada finalizada!")
