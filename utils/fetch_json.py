import json
import pandas as pd

def fetch_valid_funcionarios() -> list:
    """Fetches valid funcionarios from the JSON file."""
    try:
        with open('data/funcionarios.json', 'r') as file:
            data = json.load(file)
            return pd.DataFrame(data)
    except FileNotFoundError:
        print("Arquivo funcionarios.json não encontrado.")
        return []
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON do arquivo funcionarios.json.")
        return []
    