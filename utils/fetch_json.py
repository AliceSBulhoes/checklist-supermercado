import json
import pandas as pd

def fetch_json_data(file_path: str) -> pd.DataFrame:
    """Fetches um DataFrame a partir de um arquivo JSON."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return pd.DataFrame(data)
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return pd.DataFrame()
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o JSON do arquivo {file_path}.")
        return pd.DataFrame()