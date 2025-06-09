# Consolida os arquivos JSON baixados em um único arquivo e remove dados irrelevantes.

import os
import json
import pandas as pd
import hashlib
from bs4 import BeautifulSoup

src_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(src_dir, '..', 'data')
downloads_dir = os.path.join(data_dir, 'downloads')

def gerar_uid(df):
    str_obj = df.drop(['uid', 'edicao']).to_json(force_ascii=False)
    return hashlib.sha256(str_obj.encode('utf-8')).hexdigest()

def strip(text):
    return BeautifulSoup(text, "html.parser").get_text().strip()

def main() :
    columns = ['uid', 'edicao', 'name', 'auditorium', 'description', 'open', 'start_time', 'end_time', 'speakers']
    programacao = pd.DataFrame(columns=columns)

    for arquivoJson in sorted(os.listdir(downloads_dir)):
        if not arquivoJson.endswith('.json'):
            continue

        print(f"Processando: {arquivoJson}")

        edicaoNome = arquivoJson.split(' - ')[1].replace('-bancadas', '').replace('.json', '')

        with open(os.path.join(downloads_dir, arquivoJson), 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        for atividade in json_data['result']['schedule']:
            for item in atividade['activity_list']:
                atividadeLimpa = pd.Series({
                    'name': item['name'],
                    'auditorium': item['auditorium_name'],
                    'description': strip(item['description']),
                    'open': item['open'],
                    'start_time': item['start_time'],
                    'end_time': item['end_time'],
                    'speakers': [{'name': speaker['name'], 'profession': speaker['profession'], 'description': strip(speaker.get('description') or '')} for speaker in item['speakers']]
                }, index=columns)

                uid = gerar_uid(atividadeLimpa)

                atividadeLimpa['uid'] = uid
                atividadeLimpa['edicao'] = edicaoNome
                programacao.loc[len(programacao)] = atividadeLimpa

    programacao.drop_duplicates(subset=['uid'], inplace=True)

    programacao.to_json(os.path.join(data_dir, 'limpo.json'), orient='records', force_ascii=False, indent=2)

if __name__ == "__main__":
    main()
