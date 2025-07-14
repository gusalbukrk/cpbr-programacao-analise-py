# Faz o download dos arquivos JSON contendo a programação das últimas 10 edições da Campus Party.

import os
import json
import pandas as pd
import requests

src_dir = os.path.dirname(os.path.abspath(__file__))

downloads_dir = os.path.join(src_dir, '..', 'data', 'downloads')
os.makedirs(downloads_dir, exist_ok=True) 

def download(url, arquivoNome):
    print(f"Download em progresso: {arquivoNome}")

    data = requests.get(url).json()

    with open(os.path.join(downloads_dir, arquivoNome), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Download finalizado: {arquivoNome}")

def main() :
    metadados = pd.read_json(os.path.join(src_dir, '..', 'metadados.json'))

    for row in metadados.itertuples():
        arquivoNome = f"{row.Index} - {row.nome}.json"
        arquivoNomeBancadas = f"{row.Index} - {row.nome}-bancadas.json"

        download(row.programacaoLink, arquivoNome)

        if row.programacaoBancadasLink is not None:
            download(row.programacaoBancadasLink, arquivoNomeBancadas)

if __name__ == "__main__":
    main()