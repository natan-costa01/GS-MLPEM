
# FIAP - Global Solution 2026
# Modelagem Linear para Aprendizado em Máquina
# Professor: Rodolfo
#
# Henrique de Souza Aragão - RM 570529
# Leonardo Scotti Tobias - RM 573305
# Natan Silva da Costa - RM 573100

import pandas as pd

# 1. Carregar a base de dados
df = pd.read_csv(
    "data/uso_da_frota_2025.csv",
    sep=";",
    encoding="latin1"
)

print("Quantidade de registros:", len(df))
print("Quantidade de colunas:", len(df.columns))

# 2. Verificar os dados
print("\nPrimeiros registros:")
print(df.head())

print("\nValores ausentes:")
print(df.isnull().sum())

print("\nRegistros duplicados:", df.duplicated().sum())

# 3. Remover colunas totalmente vazias
df = df.dropna(axis=1, how="all")

# 4. Converter as colunas numéricas
colunas_numericas = [
    "KM Estimada",
    "KM Real",
    "Custo Estimado",
    "Custo Real",
    "Passageiros",
    "Ano Veículo"
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

# 5. Converter as datas
df["Data Saída"] = pd.to_datetime(
    df["Data Saída"], dayfirst=True, errors="coerce"
)

df["Data Retorno"] = pd.to_datetime(
    df["Data Retorno"], dayfirst=True, errors="coerce"
)

# 6. Identificar custos negativos
custos_negativos = (df["Custo Real"] < 0).sum()

print("\nCustos negativos:", custos_negativos)

# Criar uma coluna de custo para as análises
# Os valores negativos ficam preservados na coluna original
df["Custo Analise"] = df["Custo Real"]

df.loc[df["Custo Analise"] < 0, "Custo Analise"] = None

# 7. Criar variáveis auxiliares
df["Ano"] = df["Data Saída"].dt.year
df["Mes"] = df["Data Saída"].dt.month

df["Idade Veiculo"] = df["Ano"] - df["Ano Veículo"]

# Idade negativa indica inconsistência
df.loc[df["Idade Veiculo"] < 0, "Idade Veiculo"] = None

# Diferença entre custo real e estimado
df["Diferenca Custo"] = (
    df["Custo Analise"] - df["Custo Estimado"]
)

# 8. Verificar a base tratada
print("\nResumo estatístico:")
print(df[colunas_numericas].describe())

print("\nValores ausentes após o tratamento:")
print(df.isnull().sum())

print("\nRegistros finais:", len(df))
print("Colunas finais:", len(df.columns))

# 9. Salvar a base tratada
df.to_csv(
    "data/frota_tratada.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nBase tratada salva com sucesso!")
