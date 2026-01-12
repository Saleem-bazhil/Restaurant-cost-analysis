import pandas as p

def load_data(file_path: str) -> p.DataFrame:
    return p.read_excel(file_path)