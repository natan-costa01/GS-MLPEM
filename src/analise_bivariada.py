
# FIAP - Global Solution 2026
# Modelagem Linear para Aprendizado em Máquina
# Professor: Rodolfo
#
# Henrique de Souza Aragão - RM 570529
# Leonardo Scotti Tobias - RM 573305
# Natan Silva da Costa - RM 573100

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# 1. Carregar os dados
df = pd.read_csv("data/frota_tratada.csv", sep=";")

dados = df[["KM Real", "Custo Analise"]].dropna()
dados = dados[dados["KM Real"] > 0]

print("ANÁLISE BIVARIADA")
print("Quantidade de registros:", len(dados))

# 2. Gráfico de dispersão
sns.scatterplot(
    data=dados,
    x="KM Real",
    y="Custo Analise",
    alpha=0.3
)

plt.title("Distância percorrida x Custo da viagem")
plt.xlabel("KM Real")
plt.ylabel("Custo Real (R$)")
plt.grid(True)

plt.savefig("resultados/graficos/dispersao.png")
plt.show()

# 3. Covariância e correlação de Pearson
covariancia = dados["KM Real"].cov(dados["Custo Analise"])
correlacao = dados["KM Real"].corr(dados["Custo Analise"])

print("\nCOVARIÂNCIA E CORRELAÇÃO")
print(f"Covariância: {covariancia:.2f}")
print(f"Correlação de Pearson: {correlacao:.4f}")

# 4. Gráfico de correlação
plt.figure(figsize=(6, 5))

sns.heatmap(
    dados.corr(),
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

plt.title("Correlação de Pearson")
plt.tight_layout()

plt.savefig("resultados/graficos/correlacao_bivariada.png")
plt.show()

# 5. Regressão linear simples
x = sm.add_constant(dados["KM Real"])
y = dados["Custo Analise"]

modelo = sm.OLS(y, x).fit()

print("\nREGRESSÃO LINEAR SIMPLES")
print(modelo.summary())

a = modelo.params["const"]
b = modelo.params["KM Real"]

print("\nEQUAÇÃO DA REGRESSÃO")
print(f"Y = {a:.2f} + {b:.4f} * X")

# 6. Gráfico com reta de regressão
sns.regplot(
    data=dados,
    x="KM Real",
    y="Custo Analise",
    ci=None,
    scatter_kws={"alpha": 0.3},
    line_kws={"color": "red"}
)

plt.title("Regressão Linear - KM x Custo")
plt.xlabel("KM Real")
plt.ylabel("Custo Real (R$)")
plt.grid(True)

plt.savefig("resultados/graficos/regressao_simples.png")
plt.show()

# 7. Avaliação do modelo
print("\nAVALIAÇÃO DO MODELO")
print(f"R²: {modelo.rsquared:.4f}")
print(f"R² em porcentagem: {modelo.rsquared * 100:.2f}%")
print(f"Teste F: {modelo.fvalue:.4f}")
print(f"Valor-p: {modelo.f_pvalue:.6f}")

if modelo.f_pvalue < 0.05:
    print("Regressão estatisticamente significativa")
else:
    print("Regressão não significativa")

# 8. Previsão
km = 100
previsao = a + b * km

print("\nPREVISÃO")
print(f"Distância: {km} km")
print(f"Custo previsto: R$ {previsao:.2f}")

print("\nAnálise bivariada finalizada!")
