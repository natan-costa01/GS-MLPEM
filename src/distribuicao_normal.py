
# FIAP - Global Solution 2026
# Modelagem Linear para Aprendizado em Máquina
# Professor: Rodolfo
#
# Henrique de Souza Aragão - RM 570529
# Leonardo Scotti Tobias - RM 573305
# Natan Silva da Costa - RM 573100

print("INICIANDO DISTRIBUIÇÃO NORMAL")

import pandas as pd
from scipy.stats import norm

# 1. Carregar os dados tratados
df = pd.read_csv("data/frota_tratada.csv", sep=";")

# 2. Selecionar a variável KM Real
km = df["KM Real"].dropna()

# 3. Calcular as medidas estatísticas
media = km.mean()
mediana = km.median()
desvio = km.std(ddof=0)

print("DISTRIBUIÇÃO NORMAL - KM REAL")
print("Quantidade de registros:", len(km))
print(f"Média: {media:.2f} km")
print(f"Mediana: {mediana:.2f} km")
print(f"Desvio padrão: {desvio:.2f} km")

# 4. Item A - Probabilidade de ser menor que a média
prob_a = norm.cdf(media, loc=media, scale=desvio)

print("\nITEM A")
print(f"P(X < média) = {prob_a * 100:.2f}%")

if prob_a == 0:
    print("Evento impossível")
elif prob_a == 1:
    print("Evento certo")
else:
    print("Evento possível")

# 5. Item B - Probabilidade de ser maior que a mediana
prob_b = norm.sf(mediana, loc=media, scale=desvio)

print("\nITEM B")
print(f"P(X > mediana) = {prob_b * 100:.2f}%")

if prob_b == 0:
    print("Evento impossível")
elif prob_b == 1:
    print("Evento certo")
else:
    print("Evento possível")
