import sys
import os
import pandas as pd
import pytest

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import extract, transform

# Fixture para criar CSV de teste
@pytest.fixture
def sample_csv():
    raw_path = "data/raw"
    os.makedirs(raw_path, exist_ok=True)

    df = pd.DataFrame({
        "PedidoID": [1, 2],
        "Cliente": ["Alice", "Bob"],
        "Produto": ["Caneta", "Caderno"],
        "Quantidade": [10, 5],
        "PrecoUnitario": [1.5, 3.0],
        "Data": ["2026-02-01", "2026-02-02"]
    })
    test_file = os.path.join(raw_path, "vendas_test.csv")
    df.to_csv(test_file, index=False)

    yield

    # Limpeza após teste
    os.remove(test_file)

# Teste extract
def test_extract(sample_csv):
    df = extract()
    assert not df.empty
    assert list(df.columns) == ["PedidoID", "Cliente", "Produto", "Quantidade", "PrecoUnitario", "Data"]

# Teste transform
def test_transform(sample_csv):
    df = extract()
    df_transformed = transform(df)
    assert "ValorTotal" in df_transformed.columns
    assert "GrandeVenda" in df_transformed.columns
    assert df_transformed.loc[0, "ValorTotal"] == 10 * 1.5
    assert df_transformed.loc[1, "ValorTotal"] == 5 * 3.0
