import os
import pandas as pd
from pathlib import Path

# =====================
# ETAPA 1: EXTRAIR
# =====================
def extract() -> pd.DataFrame:
    """
    Lê todos os arquivos CSV da pasta data/raw e retorna um DataFrame único.
    """
    data_frames = []
    for file in os.listdir("data/raw"):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join("data/raw", file))
            data_frames.append(df)
    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        return pd.DataFrame()  # retorna vazio se não houver arquivos

# =====================
# ETAPA 2: TRANSFORMAR
# =====================
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica transformações nos dados:
    - Remove linhas com valores nulos
    - Calcula ValorTotal = Quantidade * PrecoUnitario
    - Converte Data para datetime
    - Cria flag GrandeVenda se ValorTotal > 20
    """
    if df.empty:
        return df

    # Remove linhas com valores nulos
    df = df.dropna()

    # Calcula valor total da venda
    df['ValorTotal'] = df['Quantidade'] * df['PrecoUnitario']

    # Converte Data para datetime
    df['Data'] = pd.to_datetime(df['Data'])

    # Cria flag de grande venda
    df['GrandeVenda'] = df['ValorTotal'] > 20

    return df

# =====================
# ETAPA 3: CARREGAR
# =====================
def load(df: pd.DataFrame):
    """
    Salva o DataFrame transformado na pasta data/processed
    """
    if df.empty:
        print("Nenhum dado para carregar.")
        return

    os.makedirs("data/processed", exist_ok=True)
    output_file = "data/processed/final.csv"
    df.to_csv(output_file, index=False)
    print(f"ETL finalizado! Dados salvos em {output_file}")

# =====================
# ORQUESTRAÇÃO
# =====================
def main():
    df = extract()
    df = transform(df)
    load(df)

if __name__ == "__main__":
    main()
