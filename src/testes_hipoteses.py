
# FIAP - Global Solution 2026
# Modelagem Linear para Aprendizado em Máquina
# Professor: Rodolfo
#
# Henrique de Souza Aragão - RM 570529
# Leonardo Scotti Tobias - RM 573305
# Natan Silva da Costa - RM 573100

import pandas as pd
import numpy as np
from scipy.stats import norm

# 1. Carregar os dados
df = pd.read_csv("data/frota_tratada.csv", sep=";")

km = df["KM Real"].dropna()

# 2. Média e desvio padrão populacional
media_pop = km.mean()
desvio_pop = km.std(ddof=0)

print("TESTES DE HIPÓTESES - KM REAL")
print(f"Média populacional: {media_pop:.2f} km")
print(f"Desvio padrão populacional: {desvio_pop:.2f} km")

# 3. TESTE A
# H0: média >= média populacional
# H1: média < média populacional

amostra_a = km.sample(n=20, random_state=42)

media_a = amostra_a.mean()
alpha_a = 0.06

z_a = (media_a - media_pop) / (desvio_pop / np.sqrt(20))
p_a = norm.cdf(z_a)

print("\nTESTE A - MÉDIA MENOR")
print(f"Média amostral: {media_a:.2f} km")
print(f"Estatística Z: {z_a:.4f}")
print(f"Valor-p: {p_a:.4f}")
print("Significância: 6%")

if p_a < alpha_a:
    print("Rejeitamos H0")
    print("Há evidências de que a média é menor.")
else:
    print("Não rejeitamos H0")
    print("Não há evidências suficientes de que a média é menor.")

# 4. TESTE B
# H0: média <= média populacional
# H1: média > média populacional

amostra_b = km.sample(n=25, random_state=44)

media_b = amostra_b.mean()
alpha_b = 0.09

z_b = (media_b - media_pop) / (desvio_pop / np.sqrt(25))
p_b = norm.sf(z_b)

print("\nTESTE B - MÉDIA MAIOR")
print(f"Média amostral: {media_b:.2f} km")
print(f"Estatística Z: {z_b:.4f}")
print(f"Valor-p: {p_b:.4f}")
print("Significância: 9%")

if p_b < alpha_b:
    print("Rejeitamos H0")
    print("Há evidências de que a média é maior.")
else:
    print("Não rejeitamos H0")
    print("Não há evidências suficientes de que a média é maior.")
