# Usa Gemini API para classificar as atividades em quatro categorias:
# eixo temático, perfil do organizador, formato da atividade e objetivo da atividade.

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
import re
import pandas as pd
from collections import Counter, defaultdict

src_dir = os.path.dirname(os.path.abspath(__file__))
categorizado_caminho = os.path.join(src_dir, "..", "data", "categorizado.json")

load_dotenv()

ai = genai.Client(api_key=os.getenv("API_KEY"))

with open(os.path.join(src_dir, "..", "prompt_template.md"), "r", encoding="utf-8") as f:
    prompt_template = f.read()

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "taxonomia.json"), 'r', encoding='utf-8') as f:
   taxonomia  = json.load(f)
#
eixos_rotulos = list(map(lambda eixo: eixo['nome'], taxonomia['eixos']))
perfis_rotulos = list(map(lambda eixo: eixo['nome'], taxonomia['perfis']))
formatos_rotulos = list(map(lambda eixo: eixo['nome'], taxonomia['formatos']))
objetivos_rotulos = list(map(lambda eixo: eixo['nome'], taxonomia['objetivos']))

def atualizar_arquivo_categorizado(data):
    try:
        with open(categorizado_caminho, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao escrever categorizado.json: {e}")

def omitir_atributos_irrelevantes(atividade: pd.Series):
    atividade_reduzida = atividade.drop(['uid', 'edicao', 'open', 'start_time', 'end_time'])
    atividade_reduzida.rename({'speakers': 'organizers'}, inplace=True)
    return atividade_reduzida

def remover_markdown_code_blocks(text):
    text = re.sub(r'^\s*```(?:json\s*)?\n*', '', text)
    text = re.sub(r'\s*```\s*$', '', text)
    return text.strip()

def obter_horario_atual():
    agora = datetime.now()
    return agora.strftime("%H:%M:%S")

def is_in(s, l):
    return s.lower() in [ el.lower() for el in l ]

def consolidar_candidatos(candidatos):
    formato_counts = Counter()
    objetivo_counts = Counter()
    perfil_organizador_counts = Counter()
    eixo_item_counts = defaultdict(int)

    for candidato in candidatos:
        if 'formato' in candidato and candidato['formato'] is not None and is_in(candidato['formato'], formatos_rotulos):
            formato_counts[candidato['formato']] += 1
        if 'objetivo' in candidato and candidato['objetivo'] is not None and is_in(candidato['objetivo'], objetivos_rotulos):
            objetivo_counts[candidato['objetivo']] += 1
        if 'perfil_organizador' in candidato and candidato['perfil_organizador'] is not None  and is_in(candidato['perfil_organizador'], perfis_rotulos):
            perfil_organizador_counts[candidato['perfil_organizador']] += 1

        if 'eixo' in candidato and isinstance(candidato['eixo'], list):
            for i, item_eixo in enumerate(candidato['eixo']):
                if is_in(item_eixo, eixos_rotulos):
                    if i == 0:
                        eixo_item_counts[item_eixo] += 3
                    elif i == 1:
                        eixo_item_counts[item_eixo] += 2
                    elif i == 2:
                        eixo_item_counts[item_eixo] += 1

    consolidado = {}

    eixos_para_ordenar = []
    for item, score in eixo_item_counts.items():
        if score >= 3:
            eixos_para_ordenar.append((item, score))
    eixos_para_ordenar.sort(key=lambda x: -x[1])
    consolidado['eixo'] = [item for item, count in eixos_para_ordenar]

    if perfil_organizador_counts:
        consolidado['perfil_organizador'] = perfil_organizador_counts.most_common(1)[0][0]
    else:
        consolidado['perfil_organizador'] = None

    if formato_counts:
        consolidado['formato'] = formato_counts.most_common(1)[0][0]
    else:
        consolidado['formato'] = None

    if objetivo_counts:
        consolidado['objetivo'] = objetivo_counts.most_common(1)[0][0]
    else:
        consolidado['objetivo'] = None

    return consolidado

def categorizar(atividade):
    prompt = f"{prompt_template}{omitir_atributos_irrelevantes(atividade).to_json(force_ascii=False)}"

    try:
        resp = ai.models.generate_content(
            # model="gemini-2.0-flash-lite",
            model="gemini-2.5-flash-preview-04-17",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                candidateCount=3,
            )
        )

        candidatos = [
            json.loads(remover_markdown_code_blocks(candidate.content.parts[0].text))
            for candidate in resp.candidates
        ]
    except Exception:
        return None

    consolidado = consolidar_candidatos(candidatos)

    return consolidado

def main():
    columns = ['uid', 'edicao', 'name', 'auditorium', 'description', 'open', 'start_time', 'end_time', 'speakers', 'eixo', 'perfil_organizador', 'formato', 'objetivo']
    
    limpo = pd.read_json(os.path.join(src_dir, "..", "data", "limpo.json"))

    try:
        categorizado = pd.read_json(categorizado_caminho)
    except Exception:
        categorizado = pd.DataFrame(columns=columns)

    atividades_quant_total = len(limpo)

    for _, atividade in limpo.iterrows():
        if (atividade.uid in categorizado["uid"].values):
            categorizado.to_json(categorizado_caminho, orient='records', force_ascii=False, indent=2)
            continue

        print(f"{obter_horario_atual()} - {len(categorizado) + 1} de {atividades_quant_total}")

        while ((categorias := categorizar(atividade)) == None):
            pass

        categorizado.loc[len(categorizado)] = {**atividade, **categorias}
        categorizado.to_json(categorizado_caminho, orient='records', force_ascii=False, indent=2)

if __name__ == "__main__":
    main()
